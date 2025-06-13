from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.models import Race, RaceCreate, RaceRead, RaceUpdate

router = APIRouter()


@router.get("/races", response_model=list[RaceRead])
def get_races(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Race]:
    """Get all races with pagination."""
    statement = select(Race).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/races/{race_id}", response_model=RaceRead)
def get_race(
    race_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Race:
    """Get a specific race by ID."""
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@router.post("/races", response_model=RaceRead)
def create_race(
    race: RaceCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Race:
    """Create a new race."""
    db_race = Race.model_validate(race)
    session.add(db_race)
    session.commit()
    session.refresh(db_race)
    return db_race


@router.put("/races/{race_id}", response_model=RaceRead)
def update_race(
    race_id: int,
    race: RaceUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Race:
    """Update a race."""
    db_race = session.get(Race, race_id)
    if not db_race:
        raise HTTPException(status_code=404, detail="Race not found")

    race_data = race.model_dump(exclude_unset=True)
    for key, value in race_data.items():
        setattr(db_race, key, value)

    session.add(db_race)
    session.commit()
    session.refresh(db_race)
    return db_race


@router.delete("/races/{race_id}")
def delete_race(
    race_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a race."""
    race = session.get(Race, race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")

    session.delete(race)
    session.commit()
    return {"message": "Race deleted successfully"}


@router.get("/races/year/{year}", response_model=list[RaceRead])
def get_races_by_year(
    year: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[Race]:
    """Get races by year."""
    statement = select(Race).where(Race.year == year)
    return list(session.exec(statement).all())
