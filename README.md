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
