"""MOCK eye test feed (results pushed by test centres). Returns the most recent result."""
from datetime import date

from core.models import EyeTest


def get_latest(session, emirates_id: str) -> dict | None:
    r = (session.query(EyeTest).filter_by(emirates_id=emirates_id)
         .order_by(EyeTest.test_date.desc(), EyeTest.id.desc()).first())
    if r is None:
        return None
    return {"centre": r.centre, "test_date": r.test_date, "passed": r.passed}


def add_record(session, emirates_id: str, centre: str, passed: bool = True, test_date: date | None = None) -> None:
    """Used by the 'Eye test completed' demo action."""
    session.add(EyeTest(emirates_id=emirates_id, centre=centre, passed=passed,
                        test_date=test_date or date.today()))
