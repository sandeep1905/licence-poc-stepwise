# Licence renewal POC (step-by-step build)

AI prepares and checks; a human officer makes every final decision. All data is synthetic.
See PLAN.md for the build steps.

## Setup (step 1)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

Tesseract (OCR engine) must be installed separately - check with `tesseract --version`:
macOS `brew install tesseract`, Ubuntu `sudo apt install tesseract-ocr`,
Windows: <https://github.com/UB-Mannheim/tesseract/wiki>.

Business rules live in `config/rules.yaml` (illustrative - verify with RTA before real use);
LLM mode and other settings in `config/settings.yaml`.

## Database and mock services (step 2)

`core/models.py` + `core/db.py`: one SQLite file (`data/licence_poc.db`, override with env var `LICENCE_DB`).
Mock government services in `integrations/`: `mock_uae_pass`, `mock_licence_db`, `mock_fines`, `mock_eye_tests`, `mock_payment`.
A citizen with no row in `licence_records` has no licence. Application tables (cases, documents, audit log...) arrive in later steps.
