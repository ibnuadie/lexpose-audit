# Graph Report - .  (2026-07-16)

## Corpus Check
- Corpus is ~7,229 words - fits in a single context window. You may not need a graph.

## Summary
- 17 nodes · 17 edges · 7 communities (2 shown, 5 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.92)
- Token cost: 1,284 input · 820 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Two-Phase Transaction Security & Implementation|Two-Phase Transaction Security & Implementation]]
- [[_COMMUNITY_Testing Blueprint & Audit Mockup Portal|Testing Blueprint & Audit Mockup Portal]]
- [[_COMMUNITY_LexCoin Ledger & Protocol Mechanics|LexCoin Ledger & Protocol Mechanics]]
- [[_COMMUNITY_B2B Enterprise Architecture|B2B Enterprise Architecture]]
- [[_COMMUNITY_Flat Pricing Model|Flat Pricing Model]]
- [[_COMMUNITY_Hybrid Pricing Model|Hybrid Pricing Model]]
- [[_COMMUNITY_Per-Item Pricing Model|Per-Item Pricing Model]]

## God Nodes (most connected - your core abstractions)
1. `Lexpose Two-Phase Transaction Sequence Diagram` - 6 edges
2. `API Gateway (LexCoin Backend)` - 5 edges
3. `Lexpose Audit Portal Home` - 4 edges
4. `Lexpose AI` - 3 edges
5. `LexCoin Usage-Based Ledger Engine` - 3 edges
6. `Ledger DB (Postgres Audit)` - 3 edges
7. `Lexpose UI (React Portal & HUD)` - 2 edges
8. `AI Worker (LLM Doc Generator)` - 2 edges
9. `Lexpose & LexCoin Audit Plan Presentation Deck` - 2 edges
10. `Two-Phase Commit Protocol` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Lexpose & LexCoin Audit Plan Presentation Deck` --conceptually_related_to--> `Lexpose AI`  [INFERRED]
  pitch-deck/index.html → docs/STRATEGIC_PLAN.md
- `Chrome DevTools MCP Automated Testing Blueprint` --conceptually_related_to--> `Lexpose Audit Portal Home`  [INFERRED]
  docs/STRATEGIC_PLAN.md → mockup/index.html
- `Lexpose Audit Portal Home` --references--> `Lexpose Two-Phase Transaction Sequence Diagram`  [EXTRACTED]
  mockup/index.html → docs/lexpose_transaction.html
- `Lexpose Audit Portal Home` --references--> `Lexpose AI`  [EXTRACTED]
  mockup/index.html → docs/STRATEGIC_PLAN.md
- `Idempotency Guard` --conceptually_related_to--> `API Gateway (LexCoin Backend)`  [INFERRED]
  docs/STRATEGIC_PLAN.md → docs/lexpose_transaction.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Two-Phase Commit Protocol Flow Participants** — docs_lexpose_transaction_lexpose_ui, docs_lexpose_transaction_api_gateway, docs_lexpose_transaction_ledger_db, docs_lexpose_transaction_ai_worker [EXTRACTED 1.00]
- **LexCoin Generation Cost Pricing Models** — docs_strategic_plan_flat_pricing, docs_strategic_plan_per_item_pricing, docs_strategic_plan_hybrid_pricing [EXTRACTED 1.00]

## Communities (7 total, 5 thin omitted)

### Community 0 - "Two-Phase Transaction Security & Implementation"
Cohesion: 0.43
Nodes (7): AI Worker (LLM Doc Generator), API Gateway (LexCoin Backend), Lexpose Two-Phase Transaction Sequence Diagram, Ledger DB (Postgres Audit), Lexpose UI (React Portal & HUD), PostgreSQL Advisory Locks, Idempotency Guard

### Community 1 - "Testing Blueprint & Audit Mockup Portal"
Cohesion: 0.67
Nodes (4): Chrome DevTools MCP Automated Testing Blueprint, Lexpose AI, Lexpose Audit Portal Home, Lexpose & LexCoin Audit Plan Presentation Deck

## Knowledge Gaps
- **7 isolated node(s):** `B2B Enterprise Wallet Architecture`, `PostgreSQL Advisory Locks`, `Idempotency Guard`, `Chrome DevTools MCP Automated Testing Blueprint`, `Flat Pricing Model` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Lexpose Two-Phase Transaction Sequence Diagram` connect `Two-Phase Transaction Security & Implementation` to `Testing Blueprint & Audit Mockup Portal`, `LexCoin Ledger & Protocol Mechanics`?**
  _High betweenness centrality (0.338) - this node is a cross-community bridge._
- **Why does `Lexpose Audit Portal Home` connect `Testing Blueprint & Audit Mockup Portal` to `Two-Phase Transaction Security & Implementation`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `LexCoin Usage-Based Ledger Engine` connect `LexCoin Ledger & Protocol Mechanics` to `Two-Phase Transaction Security & Implementation`, `Testing Blueprint & Audit Mockup Portal`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **What connects `Two-Phase Commit Protocol`, `B2B Enterprise Wallet Architecture`, `PostgreSQL Advisory Locks` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._