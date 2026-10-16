"""MOCK licence database lookup by Emirates ID."""
from core.models import LicenceRecord


def get_licence(session, emirates_id: str) -> dict | None:
    """Return the licence record as a plain dict, or None if the person has no licence."""
    r = session.query(LicenceRecord).filter_by(emirates_id=emirates_id).first()
    if r is None:
        return None
    return {
        "licence_no": r.licence_no, "category": r.category, "expiry_date": r.expiry_date,
        "status": r.status, "eye_test_linked": r.eye_test_linked,
        "id_verified": r.id_verified, "record_complete": r.record_complete,
    }


def set_expiry(session, emirates_id: str, new_expiry) -> None:
    """Called after a renewal is issued."""
    r = session.query(LicenceRecord).filter_by(emirates_id=emirates_id).first()
    if r:
        r.expiry_date = new_expiry
