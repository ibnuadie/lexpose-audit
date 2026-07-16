# test_lexpose_ai.py
# ponytail: limit 200 lines
# strict typing: full type hints used

import asyncio
import json
import re
from typing import Dict, Any
import websockets

WS_URL: str = "ws://localhost:9222/devtools/page/180D1077D3AD96F06063B5EC656D3396"

async def run_eval(ws: websockets.WebSocketClientProtocol, expression: str, retries: int = 8) -> Any:
    """Helper to run JS expressions on target page with retry support"""
    for attempt in range(retries):
        cmd_id = 100 + attempt * 10
        await ws.send(json.dumps({
            "id": cmd_id, 
            "method": "Runtime.evaluate", 
            "params": {"expression": expression, "returnByValue": True}
        }))
        
        while True:
            resp = await ws.recv()
            result = json.loads(resp)
            if result.get('id') == cmd_id:
                break
                
        res_obj = result.get('result', {})
        if "exceptionDetails" in res_obj:
            await asyncio.sleep(1.5)
            continue
            
        val = res_obj.get('result', {}).get('value')
        if val is not None:
            return val
            
        await asyncio.sleep(1.5)
    return None

async def wait_for_url(ws: websockets.WebSocketClientProtocol, pattern: str, timeout: float = 45.0) -> Dict[str, Any]:
    """Poll page URL until it contains the target pattern"""
    start_time = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start_time < timeout:
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body ? document.body.innerText : ''})")
        if page_info and pattern in page_info.get('url', ''):
            return page_info
        await asyncio.sleep(1.5)
    raise TimeoutError(f"Timed out waiting for URL pattern: {pattern}")

def get_credits_balance(text: str) -> int:
    """Extract credit balance number from page body text"""
    match = re.search(r'(\d+)\s*\n?\s*Kredit', text)
    if match:
        return int(match.group(1))
    match = re.search(r'Kredit\s*\n?\s*(\d+)', text)
    if match:
        return int(match.group(1))
    raise ValueError(f"Could not find credit balance in text: {text[:200]}")

async def test_lexia_happy_flow() -> None:
    print("[1/5] Connecting to Chrome debugger...")
    async with websockets.connect(WS_URL, max_size=10*1024*1024, ping_interval=None) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
        await ws.recv()
        
        # Step 1: Check initial page state and starting balance
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body ? document.body.innerText : ''})")
        assert "dashboard" in page_info['url'], "Test must start on dashboard page"
        
        initial_balance = get_credits_balance(page_info['text'])
        print(f"  Dashboard loaded. Starting balance: {initial_balance} Credits.")
        
        # Step 2: Click 'Mulai dengan Lexia' and accept Beta warning modal
        print("[2/5] Navigating through warning modal...")
        click_lexia_js = """
        (() => {
            const el = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('dengan Lexia') || b.textContent.trim().includes('Lexia'));
            if (el) el.click();
        })()
        """
        await run_eval(ws, click_lexia_js)
        await asyncio.sleep(1.5)
        
        click_agree_js = """
        (() => {
            const el = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Saya mengerti') || b.textContent.trim().includes('mengerti'));
            if (el) el.click();
        })()
        """
        await run_eval(ws, click_agree_js)
        
        # Verify transition to ai-drafts input page
        page_info = await wait_for_url(ws, "deskripsi-permintaan")
        print("  Lexia inputs page loaded successfully.")

        # Step 3: Fill request description and submit
        print("[3/5] Typing description and submitting...")
        type_and_submit_js = """
        (() => {
            const ta = document.querySelector('textarea');
            const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeTextAreaValueSetter.call(ta, 'Peraturan bupati tentang keterbukaan informasi publik untuk menjamin hak warga mengakses dokumen dan informasi pemerintah daerah secara transparan.');
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Kembangkan'));
            if (btn) btn.click();
        })()
        """
        await run_eval(ws, type_and_submit_js)
        
        # Step 4: Verify brief generation and submit structure config
        print("[4/5] Reviewing AI brief and starting compilation...")
        page_info = await wait_for_url(ws, "drafting-brief-normatif")
        
        balance_after_reserve = get_credits_balance(page_info['text'])
        print(f"  Base reservation cost verified. Balance: {balance_after_reserve} Credits.")
        assert balance_after_reserve == initial_balance - 10, f"Reservation deduction mismatch! Expected {initial_balance - 10}, got {balance_after_reserve}"
        
        # Select brief options and submit
        submit_brief_js = """
        (() => {
            const clickRadio = (name, val) => {
                const el = document.querySelector(`input[type="radio"][name="${name}"][value="${val}"]`);
                if (el) { el.click(); el.dispatchEvent(new Event('change', { bubbles: true })); }
            };
            clickRadio('jenis_dokumen', 'peraturan');
            clickRadio('otoritas', 'bupati_kabupaten_placeholder');
            const selectAll = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Pilih semua'));
            if (selectAll) selectAll.click();
            const submit = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Susun Kerangka'));
            if (submit) submit.click();
        })()
        """
        await run_eval(ws, submit_brief_js)
        
        # Poll and bypass warning modal until URL transitions to draft-struktur
        print("  Bypassing brief warning modal...")
        start_time = asyncio.get_event_loop().time()
        bypassed_brief = False
        while asyncio.get_event_loop().time() - start_time < 120.0:
            page_info = await run_eval(ws, "({url: window.location.href, text: document.body ? document.body.innerText : ''})")
            if "draft-struktur" in page_info.get('url', ''):
                bypassed_brief = True
                break
            
            # Click Lanjutkan to bypass placeholders
            await run_eval(ws, "(() => { const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.trim().includes('Lanjutkan')); if (b) b.click(); })()")
            await asyncio.sleep(2)
            
        assert bypassed_brief, "Failed to navigate to draft-struktur within timeout"
        
        # Step 5: Manual Pasal 1 injection and finalize
        print("[5/5] Injecting manual Pasal 1 definitions and finalising...")
        balance_after_deduct = get_credits_balance(page_info['text'])
        print(f"  Variable cost verification. Balance: {balance_after_deduct} Credits.")
        assert balance_after_deduct == initial_balance - 15, f"Variable cost deduction mismatch! Expected {initial_balance - 15}, got {balance_after_deduct}"
        
        # Fill Pasal 1 definitions and finalize
        finalize_js = """
        (() => {
            const ta = Array.from(document.querySelectorAll('textarea')).find(el => el.placeholder === 'Teks pasal...');
            const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeTextAreaValueSetter.call(ta, 'Pasal 1: Ketentuan Umum (Informasi Publik, Badan Publik, Pemohon Informasi, Pejabat Pengelola Informasi dan Dokumentasi).');
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Finalisasi'));
            if (btn) btn.click();
        })()
        """
        await run_eval(ws, finalize_js)
        
        # Poll and confirm incomplete finalization warnings until URL transitions to dokumen-final-regulasi
        print("  Bypassing finalization warning modal...")
        start_time = asyncio.get_event_loop().time()
        finalized = False
        while asyncio.get_event_loop().time() - start_time < 60.0:
            page_info = await run_eval(ws, "({url: window.location.href})")
            if "dokumen-final-regulasi" in page_info.get('url', ''):
                finalized = True
                break
                
            # Click Lanjutkan
            await run_eval(ws, "(() => { const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.trim().includes('Lanjutkan')); if (b) b.click(); })()")
            await asyncio.sleep(2)
            
        assert finalized, "Failed to navigate to dokumen-final-regulasi within timeout"
        
        # Transition to main editor
        editor_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Lanjut ke LexPose') || b.textContent.trim().includes('Editor'));
            if (btn) btn.click();
        })()
        """
        await run_eval(ws, editor_js)
        
        # Poll and click Tetap Lanjut editor bypass warnings until URL transitions to documents-editor
        print("  Transitioning to live Document Editor...")
        start_time = asyncio.get_event_loop().time()
        entered_editor = False
        while asyncio.get_event_loop().time() - start_time < 60.0:
            page_info = await run_eval(ws, "({url: window.location.href})")
            if "documents-editor" in page_info.get('url', ''):
                entered_editor = True
                break
                
            # Click Tetap Lanjut
            await run_eval(ws, "(() => { const b = Array.from(document.querySelectorAll('button')).find(el => el.textContent.trim().includes('Tetap Lanjut') || el.textContent.trim().includes('Editor')); if (b) b.click(); })()")
            await asyncio.sleep(2)
            
        assert entered_editor, "Failed to reach final Editor Workspace within timeout"
        print("🎉 SUCCESS: Happy path automation test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_lexia_happy_flow())
