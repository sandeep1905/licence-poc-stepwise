"""Shared test setup: every test gets a fresh empty SQLite database."""
import os
from datetime import date, timedelta

import pytest

os.environ["LLM_MODE"] = "fallback"   # tests never call an LLM

from core import config, db
from core.models import Citizen, EyeTest, Fine, LicenceRecord

TODAY = date.today()


@pytest.fixture()
def session(tmp_path, monkeypatch):
    monkeypatch.setenv("LICENCE_DB", str(tmp_path / "test.db"))
    config.reload()
    s = db.new_session()
    yield s
    s.close()


@pytest.fixture()
def make_citizen(session):
    """Factory: make_citizen(...) creates a citizen with a licence, valid eye test and no fines by default."""
    counter = {"n": 0}

    def _make(licence_expiry=None, fines=0.0, eye="valid", status="ACTIVE", has_licence=True,
              eid_expiry=None, flags=None, name="Test Person"):
        counter["n"] += 1
        eid = f"784-1990-{1000000 + counter['n']}-1"
        c = Citizen(name=name, emirates_id=eid, eid_expiry=eid_expiry or TODAY + timedelta(days=500),
                    phone=f"+97150000{counter['n']:04d}", scenario="test", expected_outcome="ISSUED", sim={})
        session.add(c)
        if has_licence:
            session.add(LicenceRecord(emirates_id=eid, licence_no=f"DXB-{2000000 + counter['n']}", category="Light Vehicle",
                                      expiry_date=licence_expiry or TODAY + timedelta(days=100), status=status,
                                      **(flags or {})))
            session.add(Fine(emirates_id=eid, amount_aed=fines))
        rules = config.get_rules()
        if eye in ("valid", "failed"):
            session.add(EyeTest(emirates_id=eid, centre=rules["approved_eye_test_centres"][0],
                                test_date=TODAY - timedelta(days=100), passed=(eye == "valid")))
        session.commit()
        return c
    return _make
