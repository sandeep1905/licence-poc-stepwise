"""MOCK of the UAE Pass identity service. Authentication itself is added in step 10."""
from core.models import Citizen


def list_citizens(session) -> list[Citizen]:
    return session.query(Citizen).order_by(Citizen.id).all()


def get_profile(session, citizen_id: int) -> Citizen | None:
    return session.get(Citizen, citizen_id)


def get_profile_by_eid(session, emirates_id: str) -> Citizen | None:
    return session.query(Citizen).filter_by(emirates_id=emirates_id).first()
