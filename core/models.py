"""SQLAlchemy tables.

Step 2 covers the MOCK GOVERNMENT data only (identity, licence, fines, eye tests, payments).
Application tables (cases, documents, audit log, chat, SMS, sessions) are added in later steps.
"""
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Citizen(Base):
    """What mock UAE Pass knows about a person (+ labels used by the synthetic test data)."""
    __tablename__ = "citizens"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    emirates_id = Column(String, unique=True, nullable=False)
    eid_expiry = Column(Date, nullable=False)
    phone = Column(String)
    scenario = Column(String)              # which test scenario this synthetic person covers
    expected_outcome = Column(String)      # label for batch evaluation (final state)
    sim = Column(JSON)                     # scripted behaviour for batch evaluation


class LicenceRecord(Base):
    """Mock licence database. A citizen with no row here has no licence."""
    __tablename__ = "licence_records"
    id = Column(Integer, primary_key=True)
    emirates_id = Column(String, unique=True, index=True)
    licence_no = Column(String)
    category = Column(String)
    expiry_date = Column(Date)
    status = Column(String, default="ACTIVE")   # ACTIVE / SUSPENDED
    # flags that decide which documents are still needed
    eye_test_linked = Column(Boolean, default=True)
    id_verified = Column(Boolean, default=True)
    record_complete = Column(Boolean, default=True)


class Fine(Base):
    __tablename__ = "fines"
    id = Column(Integer, primary_key=True)
    emirates_id = Column(String, unique=True, index=True)
    amount_aed = Column(Float, default=0)


class EyeTest(Base):
    __tablename__ = "eye_tests"
    id = Column(Integer, primary_key=True)
    emirates_id = Column(String, index=True)
    centre = Column(String)
    test_date = Column(Date)
    passed = Column(Boolean, default=True)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    txn_id = Column(String, unique=True)
    emirates_id = Column(String)
    case_id = Column(Integer, nullable=True)
    purpose = Column(String)               # FINES / RENEWAL_FEE
    amount_aed = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
