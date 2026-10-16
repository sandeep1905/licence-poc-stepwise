# Licence renewal POC - step-by-step build

We build one step at a time. Each step ends with working, tested code, then we pause for review.

| # | Step | Result you can see |
|---|------|--------------------|
| 1 | Project setup: venv, requirements, config files ✅ | `pytest` runs, config loads |
| 2 | Database + mock integrations (UAE Pass, licence DB, fines, eye tests, payment) | Tables created |
| 3 | Synthetic data: 50 citizens + sample documents | Data in DB, sample images |
| 4 | Rules engine (eligibility, late fee, eye test, checklist) | Unit tests pass |
| 5 | Case state machine + audit log | Cases move through states |
| 6 | Document AI (OCR, quality, matching, tamper hints) | Scores per document |
| 7 | Confidence gate | Gate decisions tested |
| 8 | Policy RAG + intent | Questions answered |
| 9 | LangGraph agents + draft assessor | Agent paths logged |
| 10 | Authentication (simulated UAE PASS, staff, lockout) | Sign-in works |
| 11 | FastAPI service | `/docs` works |
| 12 | Streamlit UI (citizen, officer, dashboard) | Screens in browser |
| 13 | Batch evaluation + README | 50 cases end to end |

Status: **step 1 done** - waiting for "go" on step 2.
