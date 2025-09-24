"""Database session management."""

from sqlalchemy.orm import Session
from typing import Generator

from app.db.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
