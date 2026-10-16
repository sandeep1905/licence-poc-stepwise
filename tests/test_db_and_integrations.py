"""Step 2 tests: database helpers and the mock government services."""
from datetime import date, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from core import db
from core.models import Citizen, Payment
from integrations import mock_eye_tests, mock_fines, mock_licence_db, mock_payment, mock_uae_pass

TODAY = date.today()


# ---------- database ----------
def test_tables_are_created_in_a_fresh_database(session):
    from sqlalchemy import inspect
    names = set(inspect(db.get_engine()).get_table_names())
    assert {"citizens", "licence_records", "fines", "eye_tests", "payments"} <= names


def test_each_test_gets_its_own_database(session, tmp_path):
    assert db.db_path() == tmp_path / "test.db"
    assert session.query(Citizen).count() == 0


def test_session_scope_commits_and_rolls_back(session):
    with db.session_scope() as s:
        s.add(Citizen(name="A B", emirates_id="784-1990-0000001-1", eid_expiry=TODAY))
    assert session.query(Citizen).count() == 1
    with pytest.raises(RuntimeError):
        with db.session_scope() as s:
            s.add(Citizen(name="C D", emirates_id="784-1990-0000002-1", eid_expiry=TODAY))
            raise RuntimeError("boom")
    assert session.query(Citizen).count() == 1          # second insert was rolled back


def test_emirates_id_is_unique(session, make_citizen):
    c = make_citizen()
    session.add(Citizen(name="Dup", emirates_id=c.emirates_id, eid_expiry=TODAY))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_reset_db_empties_everything(session, make_citizen):
    make_citizen()
    db.reset_db()
    assert db.new_session().query(Citizen).count() == 0


# ---------- mock UAE Pass ----------
def test_uae_pass_lookup(session, make_citizen):
    c = make_citizen(name="Aisha Test")
    assert mock_uae_pass.get_profile_by_eid(session, c.emirates_id).name == "Aisha Test"
    assert mock_uae_pass.get_profile(session, c.id).emirates_id == c.emirates_id
    assert mock_uae_pass.get_profile_by_eid(session, "784-0000-0000000-0") is None
    assert [x.id for x in mock_uae_pass.list_citizens(session)] == [c.id]


# ---------- mock licence DB ----------
def test_licence_lookup_returns_plain_dict(session, make_citizen):
    c = make_citizen(flags={"id_verified": False})
    rec = mock_licence_db.get_licence(session, c.emirates_id)
    assert rec["status"] == "ACTIVE" and rec["id_verified"] is False and rec["eye_test_linked"] is True
    assert isinstance(rec["expiry_date"], date)


def test_no_licence_record_returns_none(session, make_citizen):
    assert mock_licence_db.get_licence(session, make_citizen(has_licence=False).emirates_id) is None


def test_set_expiry_updates_record(session, make_citizen):
    c = make_citizen()
    new = TODAY + timedelta(days=3650)
    mock_licence_db.set_expiry(session, c.emirates_id, new)
    session.commit()
    assert mock_licence_db.get_licence(session, c.emirates_id)["expiry_date"] == new


# ---------- mock fines ----------
def test_fines_get_and_clear(session, make_citizen):
    c = make_citizen(fines=450)
    assert mock_fines.get_fines(session, c.emirates_id) == 450.0
    mock_fines.clear_fines(session, c.emirates_id)
    session.commit()
    assert mock_fines.get_fines(session, c.emirates_id) == 0.0


def test_unknown_person_has_no_fines(session):
    assert mock_fines.get_fines(session, "784-0000-0000000-0") == 0.0


# ---------- mock eye tests ----------
def test_eye_test_latest_and_missing(session, make_citizen):
    assert mock_eye_tests.get_latest(session, make_citizen(eye="valid").emirates_id)["passed"] is True
    assert mock_eye_tests.get_latest(session, make_citizen(eye="none").emirates_id) is None
    assert mock_eye_tests.get_latest(session, make_citizen(eye="failed").emirates_id)["passed"] is False


def test_add_eye_test_record_becomes_latest(session, make_citizen):
    c = make_citizen(eye="failed")
    mock_eye_tests.add_record(session, c.emirates_id, "Sample Vision Centre B", passed=True)
    session.commit()
    latest = mock_eye_tests.get_latest(session, c.emirates_id)
    assert latest["passed"] is True and latest["centre"] == "Sample Vision Centre B" and latest["test_date"] == TODAY


# ---------- mock payment ----------
def test_payment_returns_receipt_and_stores_row(session, make_citizen):
    c = make_citizen()
    txn = mock_payment.pay(session, c.emirates_id, 330, "RENEWAL_FEE", case_id=7)
    session.commit()
    assert txn.startswith("SYN-")
    row = session.query(Payment).filter_by(txn_id=txn).one()
    assert row.amount_aed == 330 and row.purpose == "RENEWAL_FEE" and row.case_id == 7


def test_receipts_are_unique(session, make_citizen):
    c = make_citizen()
    assert len({mock_payment.pay(session, c.emirates_id, 1, "FINES") for _ in range(50)}) == 50
