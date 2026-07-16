# test_lexpose_ai.py
# ponytail: limit 120 lines
# strict typing: full type hints used

import asyncio
import json
from typing import Dict, Any, List
import websockets

WS_URL: str = "ws://localhost:9222/devtools/page/180D1077D3AD96F06063B5EC656D3396"

async def run_eval(ws: websockets.WebSocketClientProtocol, expression: str, retries: int = 8) -> Any:
    """Helper to run JS expressions on target page with retry support"""
    for attempt in range(retries):
        await ws.send(json.dumps({
            "id": 100 + attempt, 
            "method": "Runtime.evaluate", 
            "params": {"expression": expression, "returnByValue": True}
        }))
        resp = await ws.recv()
        result = json.loads(resp)
        res_obj = result.get('result', {})
        
        if "exceptionDetails" in res_obj:
            # Wait and retry if DOM is not ready
            await asyncio.sleep(1.5)
            continue
            
        val = res_obj.get('result', {}).get('value')
        if val is not None:
            return val
            
        await asyncio.sleep(1.5)
    return None

async def test_lexia_happy_flow() -> None:
    print("[1/5] Connecting to Chrome debugger...")
    async with websockets.connect(WS_URL, max_size=10*1024*1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
        await ws.recv()
        
        # Step 1: Check initial page state
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body.innerText})")
        assert "dashboard" in page_info['url'], "Test must start on dashboard page"
        print("  Dashboard loaded. HUD Credits:", "503" if "503" in page_info['text'] else "Unknown")
        
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
        await asyncio.sleep(4)
        
        # Verify transition to ai-drafts input page
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body.innerText})")
        assert "deskripsi-permintaan" in page_info['url'], "Failed to navigate to AI drafts deskripsi-permintaan"
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
        await asyncio.sleep(8)
        
        # Step 4: Verify brief generation and submit structure config
        print("[4/5] Reviewing AI brief and starting compilation...")
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body.innerText})")
        assert "drafting-brief-normatif" in page_info['url'], "Failed to load brief configuration page"
        assert "493" in page_info['text'], "Base 10 credits deduction verification failed"
        print("  Base reservation cost (10 credits) verified. Balance: 493.")
        
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
        await asyncio.sleep(2)
        
        # Bypass placeholder warning
        bypass_warning_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Lanjutkan'));
            if (btn) btn.click();
        })()
        """
        await run_eval(ws, bypass_warning_js)
        print("  Bypassed brief configurations warnings.")
        await asyncio.sleep(12)
        
        # Step 5: Manual Pasal 1 injection and finalize
        print("[5/5] Injecting manual Pasal 1 definitions and finalising...")
        page_info = await run_eval(ws, "({url: window.location.href, text: document.body.innerText})")
        assert "draft-struktur" in page_info['url'], "Failed to load outline structure page"
        assert "488" in page_info['text'], "Variable cost deduction verification failed"
        print("  Variable cost (5 credits) verified. Balance: 488.")
        
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
        await asyncio.sleep(2)
        
        # Confirm incomplete finalization
        await run_eval(ws, "Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Lanjutkan')).click()")
        await asyncio.sleep(8)
        
        # Transition to main editor
        editor_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Lanjut ke LexPose') || b.textContent.trim().includes('Editor'));
            if (btn) btn.click();
        })()
        """
        await run_eval(ws, editor_js)
        await asyncio.sleep(2)
        
        # Bypass editor warnings
        await run_eval(ws, "Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim().includes('Tetap Lanjut') || b.textContent.trim().includes('Editor')).click()")
        await asyncio.sleep(8)
        
        # Final Editor check
        page_info = await run_eval(ws, "({url: window.location.href})")
        assert "documents-editor" in page_info['url'], "Verification failed: Did not reach final Editor Workspace"
        print("🎉 SUCCESS: Happy path automation test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_lexia_happy_flow())
