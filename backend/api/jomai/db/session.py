from typing import Generator

from jomai.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session: Session
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
