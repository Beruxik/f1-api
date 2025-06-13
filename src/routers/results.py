from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.models import Result, ResultCreate, ResultRead, ResultUpdate

router = APIRouter()


@router.get("/results", response_model=list[ResultRead])
def get_results(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Result]:
    """Get all results with pagination."""
    statement = select(Result).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/results/{result_id}", response_model=ResultRead)
def get_result(
    result_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Result:
    """Get a specific result by ID."""
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.post("/results", response_model=ResultRead)
def create_result(
    result: ResultCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Result:
    """Create a new result."""
    db_result = Result.model_validate(result)
    session.add(db_result)
    session.commit()
    session.refresh(db_result)
    return db_result


@router.put("/results/{result_id}", response_model=ResultRead)
def update_result(
    result_id: int,
    result: ResultUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Result:
    """Update a result."""
    db_result = session.get(Result, result_id)
    if not db_result:
        raise HTTPException(status_code=404, detail="Result not found")

    result_data = result.model_dump(exclude_unset=True)
    for key, value in result_data.items():
        setattr(db_result, key, value)

    session.add(db_result)
    session.commit()
    session.refresh(db_result)
    return db_result


@router.delete("/results/{result_id}")
def delete_result(
    result_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a result."""
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    session.delete(result)
    session.commit()
    return {"message": "Result deleted successfully"}


@router.get("/results/race/{race_id}", response_model=list[ResultRead])
def get_results_by_race(
    race_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[Result]:
    """Get results by race ID."""
    statement = select(Result).where(Result.race_id == race_id)
    return list(session.exec(statement).all())


@router.get("/results/driver/{driver_id}", response_model=list[ResultRead])
def get_results_by_driver(
    driver_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[Result]:
    """Get results by driver ID."""
    statement = select(Result).where(Result.driver_id == driver_id)
    return list(session.exec(statement).all())
