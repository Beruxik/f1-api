from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from src.database import get_session
from src.models import Driver, DriverCreate, DriverRead, DriverUpdate

router = APIRouter()


@router.get("/drivers", response_model=list[DriverRead])
def get_drivers(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Driver]:
    """Get all drivers with pagination."""
    statement = select(Driver).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/drivers/{driver_id}", response_model=DriverRead)
def get_driver(
    driver_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Driver:
    """Get a specific driver by ID."""
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.post("/drivers", response_model=DriverRead)
def create_driver(
    driver: DriverCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Driver:
    """Create a new driver."""
    db_driver = Driver.model_validate(driver)
    session.add(db_driver)
    session.commit()
    session.refresh(db_driver)
    return db_driver


@router.put("/drivers/{driver_id}", response_model=DriverRead)
def update_driver(
    driver_id: int,
    driver: DriverUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Driver:
    """Update a driver."""
    db_driver = session.get(Driver, driver_id)
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    driver_data = driver.model_dump(exclude_unset=True)
    for key, value in driver_data.items():
        setattr(db_driver, key, value)

    session.add(db_driver)
    session.commit()
    session.refresh(db_driver)
    return db_driver


@router.delete("/drivers/{driver_id}")
def delete_driver(
    driver_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a driver."""
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    session.delete(driver)
    session.commit()
    return {"message": "Driver deleted successfully"}


@router.get("/drivers/search/{nationality}", response_model=list[DriverRead])
def get_drivers_by_nationality(
    nationality: str,
    session: Annotated[Session, Depends(get_session)],
) -> list[Driver]:
    """Get drivers by nationality (case-insensitive)."""
    statement = select(Driver).where(
        func.lower(Driver.nationality) == func.lower(nationality),
    )
    return list(session.exec(statement).all())


@router.get("/drivers/search/name/{name}", response_model=list[DriverRead])
def search_drivers_by_name(
    name: str,
    session: Annotated[Session, Depends(get_session)],
) -> list[Driver]:
    """Search drivers by name (case-insensitive partial match)."""
    statement = select(Driver).where(
        (func.lower(Driver.surname).like(f"%{name.lower()}%"))
        | (func.lower(Driver.forename).like(f"%{name.lower()}%")),
    )
    return list(session.exec(statement).all())
