# ⚖️ Lexpose: Strategic Audit & Browser Testing Plan

This strategic document outlines the system mission, business logic, document classifications, and risk vectors for the **Lexpose (AI Legal Document Generation)** platform. It is designed to act as the primary operational blueprint for future testing and inspection sessions.

---

## 🏛️ 1. System Mission & Context
**Lexpose** is a web application designed to automate high-fidelity legal and legislative document drafting (e.g. Environmental Impact Analyses, Bylaws, Decrees, and Regulation Articles). 

* **The Core Rule**: Users must utilize available **Kredit** (Credits) to invoke AI generation.
* **Soft Currency**: Users can earn **Poin** (Reward Points) through system engagement, which can be converted to Kredit (10 Poin = 1 Kredit, up to 300 Kredit/month).

---

## ⚙️ 2. Core Business Logic & Pricing Models
To handle different types of documents and analysis tasks, the engine calculates generation costs using three distinct pricing algorithms:

1. **Flat Pricing**: Fixed cost per task (e.g. running a complex `Analisis Dampak Lingkungan` costs a flat 20 Kredit).
2. **Per-Item Pricing**: Cost directly proportional to outputs (e.g. generating `Pasal` or regulation articles costs 2 Kredit per article).
3. **Hybrid Pricing**: Flat base cost + per-item variable cost (e.g. drafting a custom legislative `Draft` costs a base 10 Kredit plus 5 Kredit for outline compilation).

---

## 🚨 3. Risk Vectors & Critical Paths to Audit
The testing phase must actively focus on breaking the following integration points:

* **Concurrency & Race Conditions**:
  * *The Threat*: A user fires 15 simultaneous document generation requests in parallel. If the database checks the balance concurrently, it might allow all 15 to run, leading to a negative balance.
* **Idempotency Failures**:
  * *The Threat*: A user double-clicks the "Generate" button. The server must ignore the duplicate request without double-charging or running duplicate AI calls.
* **UI HUD Desynchronization**:
  * *The Threat*: Credit balances shown in the top navigation HUD or checkout widget lag behind the database ledger status, causing user confusion.

---

## 🌐 4. Chrome DevTools Automated Testing Blueprint
The hands-on browser testing follows these verification stages:

1. **Verify Chrome Debug Connection**:
   * Query the debugging port `http://localhost:9222/json` to target the active tab.
2. **Access the Execution Portal**:
   * Perform step-by-step UI actions (Mulai -> warning Modal -> brief formulation -> structural framework -> preview -> main editor workspace).
3. **Execute Simulation Scenarios**:
   * Verify that credit reservation and deductions (base 10 credits flat + 5 credits variable) update correctly in the top nav HUD.
4. **Capture State Screenshots**:
   * Take screenshots of the form configuration, progress indicators, brief parameters, and workspace editor.
