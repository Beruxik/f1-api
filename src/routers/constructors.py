from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from src.database import get_session
from src.models import (
    Constructor,
    ConstructorCreate,
    ConstructorRead,
    ConstructorUpdate,
)

router = APIRouter()


@router.get("/constructors", response_model=list[ConstructorRead])
def get_constructors(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Constructor]:
    """Get all constructors with pagination."""
    statement = select(Constructor).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/constructors/{constructor_id}", response_model=ConstructorRead)
def get_constructor(
    constructor_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Constructor:
    """Get a specific constructor by ID."""
    constructor = session.get(Constructor, constructor_id)
    if not constructor:
        raise HTTPException(status_code=404, detail="Constructor not found")
    return constructor


@router.post("/constructors", response_model=ConstructorRead)
def create_constructor(
    constructor: ConstructorCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Constructor:
    """Create a new constructor."""
    db_constructor = Constructor.model_validate(constructor)
    session.add(db_constructor)
    session.commit()
    session.refresh(db_constructor)
    return db_constructor


@router.put("/constructors/{constructor_id}", response_model=ConstructorRead)
def update_constructor(
    constructor_id: int,
    constructor: ConstructorUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Constructor:
    """Update a constructor."""
    db_constructor = session.get(Constructor, constructor_id)
    if not db_constructor:
        raise HTTPException(status_code=404, detail="Constructor not found")

    constructor_data = constructor.model_dump(exclude_unset=True)
    for key, value in constructor_data.items():
        setattr(db_constructor, key, value)

    session.add(db_constructor)
    session.commit()
    session.refresh(db_constructor)
    return db_constructor


@router.delete("/constructors/{constructor_id}")
def delete_constructor(
    constructor_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a constructor."""
    constructor = session.get(Constructor, constructor_id)
    if not constructor:
        raise HTTPException(status_code=404, detail="Constructor not found")

    session.delete(constructor)
    session.commit()
    return {"message": "Constructor deleted successfully"}


@router.get(
    "/constructors/search/{nationality}",
    response_model=list[ConstructorRead],
)
def get_constructors_by_nationality(
    nationality: str,
    session: Annotated[Session, Depends(get_session)],
) -> list[Constructor]:
    """Get constructors by nationality."""
    statement = select(Constructor).where(
        func.lower(Constructor.nationality).like(f"%{nationality.lower()}%"),
    )
    return list(session.exec(statement).all())
