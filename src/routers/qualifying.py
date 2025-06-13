from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.models import (
    Qualifying,
    QualifyingCreate,
    QualifyingRead,
    QualifyingUpdate,
)

router = APIRouter()


@router.get("/qualifying", response_model=list[QualifyingRead])
def get_qualifying(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Qualifying]:
    """Get all qualifying results with pagination."""
    statement = select(Qualifying).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/qualifying/{qualify_id}", response_model=QualifyingRead)
def get_qualifying_result(
    qualify_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Qualifying:
    """Get a specific qualifying result by ID."""
    qualifying = session.get(Qualifying, qualify_id)
    if not qualifying:
        raise HTTPException(
            status_code=404,
            detail="Qualifying result not found",
        )
    return qualifying


@router.post("/qualifying", response_model=QualifyingRead)
def create_qualifying(
    qualifying: QualifyingCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Qualifying:
    """Create a new qualifying result."""
    db_qualifying = Qualifying.model_validate(qualifying)
    session.add(db_qualifying)
    session.commit()
    session.refresh(db_qualifying)
    return db_qualifying


@router.put("/qualifying/{qualify_id}", response_model=QualifyingRead)
def update_qualifying(
    qualify_id: int,
    qualifying: QualifyingUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Qualifying:
    """Update a qualifying result."""
    db_qualifying = session.get(Qualifying, qualify_id)
    if not db_qualifying:
        raise HTTPException(
            status_code=404,
            detail="Qualifying result not found",
        )

    qualifying_data = qualifying.model_dump(exclude_unset=True)
    for key, value in qualifying_data.items():
        setattr(db_qualifying, key, value)

    session.add(db_qualifying)
    session.commit()
    session.refresh(db_qualifying)
    return db_qualifying


@router.delete("/qualifying/{qualify_id}")
def delete_qualifying(
    qualify_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a qualifying result."""
    qualifying = session.get(Qualifying, qualify_id)
    if not qualifying:
        raise HTTPException(
            status_code=404,
            detail="Qualifying result not found",
        )

    session.delete(qualifying)
    session.commit()
    return {"message": "Qualifying result deleted successfully"}


@router.get("/qualifying/race/{race_id}", response_model=list[QualifyingRead])
def get_qualifying_by_race(
    race_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[Qualifying]:
    """Get qualifying results by race ID."""
    statement = select(Qualifying).where(Qualifying.race_id == race_id)
    return list(session.exec(statement).all())
