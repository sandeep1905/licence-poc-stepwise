"""MOCK traffic fines system."""
from core.models import Fine


def get_fines(session, emirates_id: str) -> float:
    f = session.query(Fine).filter_by(emirates_id=emirates_id).first()
    return float(f.amount_aed) if f else 0.0


def clear_fines(session, emirates_id: str) -> None:
    f = session.query(Fine).filter_by(emirates_id=emirates_id).first()
    if f:
        f.amount_aed = 0
