"""MOCK payment gateway. Always succeeds and stores a receipt."""
import uuid

from core.models import Payment


def pay(session, emirates_id: str, amount_aed: float, purpose: str, case_id: int | None = None) -> str:
    """Returns the receipt (transaction) number."""
    txn = "SYN-" + uuid.uuid4().hex[:10].upper()
    session.add(Payment(txn_id=txn, emirates_id=emirates_id, case_id=case_id,
                        purpose=purpose, amount_aed=amount_aed))
    return txn
