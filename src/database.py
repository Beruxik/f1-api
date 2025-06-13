import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./f1_data.db")

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Create database and all tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    """Get database session."""
    with Session(engine) as session:
        yield session
