"""Database helpers. One SQLite file; override its location with the env var LICENCE_DB (used by tests/batch)."""
import os
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import ROOT
from core.models import Base

DEFAULT_DB = ROOT / "data" / "licence_poc.db"
_engines: dict = {}


def db_path() -> Path:
    return Path(os.getenv("LICENCE_DB", DEFAULT_DB))


def get_engine(path: Path | str | None = None):
    """One engine per database file; tables are created on first use."""
    path = str(path or db_path())
    if path not in _engines:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        eng = create_engine(f"sqlite:///{path}", future=True,
                            connect_args={"check_same_thread": False})   # shared by web threads
        Base.metadata.create_all(eng)
        _engines[path] = eng
    return _engines[path]


def new_session(path: Path | str | None = None):
    """Plain session; the caller must close it."""
    return sessionmaker(bind=get_engine(path), expire_on_commit=False, future=True)()


@contextmanager
def session_scope(path: Path | str | None = None):
    """Commit on success, roll back on error, always close."""
    s = new_session(path)
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def reset_db(path: Path | str | None = None):
    """Drop and recreate every table (used by the data generator and tests)."""
    eng = get_engine(path)
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
