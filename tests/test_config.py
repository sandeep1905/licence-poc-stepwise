"""Step 1 tests: configuration loads and is sane."""
import pytest

from core import config


def test_rules_load_with_expected_values():
    r = config.get_rules()
    assert r["renewal_fee_aed"] == 300 and r["eye_test_validity_years"] == 3
    assert r["max_upload_attempts"] == 3 and r["confidence_threshold"] == 0.60


def test_score_weights_sum_to_one():
    assert abs(sum(config.get_rules()["score_weights"].values()) - 1.0) < 1e-9


def test_critical_cap_is_below_threshold():
    r = config.get_rules()
    assert r["critical_fail_cap"] < r["confidence_threshold"]


def test_critical_checks_are_known_names():
    r = config.get_rules()
    known = set(r["score_weights"]) | {"present"}
    assert set(r["critical_checks"]) <= known


def test_rules_file_carries_verify_warning():
    text = (config.CONFIG_DIR / "rules.yaml").read_text().lower()
    assert "verify with rta" in text


def test_llm_mode_env_override(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "FALLBACK")
    config.reload()
    assert config.get_settings()["llm_mode"] == "fallback"
    monkeypatch.delenv("LLM_MODE")
    config.reload()
    assert config.get_settings()["llm_mode"] == "auto"


def test_project_folders_exist():
    for d in ["config", "core", "tests", "data/policies", "data/sample_docs", "data/uploads", "integrations", "scripts"]:
        assert (config.ROOT / d).is_dir(), d


def test_tesseract_is_installed():
    import shutil
    if shutil.which("tesseract") is None:
        pytest.fail("Tesseract is not installed. macOS: brew install tesseract | Ubuntu: sudo apt install tesseract-ocr")
