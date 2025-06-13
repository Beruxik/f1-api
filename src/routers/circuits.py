from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from src.database import get_session
from src.models import Circuit, CircuitCreate, CircuitRead, CircuitUpdate

router = APIRouter()


@router.get("/circuits", response_model=list[CircuitRead])
def get_circuits(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> list[Circuit]:
    """Get all circuits with pagination."""
    statement = select(Circuit).offset(skip).limit(limit)
    return list(session.exec(statement).all())


@router.get("/circuits/{circuit_id}", response_model=CircuitRead)
def get_circuit(
    circuit_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Circuit:
    """Get a specific circuit by ID."""
    circuit = session.get(Circuit, circuit_id)
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit


@router.post("/circuits", response_model=CircuitRead)
def create_circuit(
    circuit: CircuitCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Circuit:
    """Create a new circuit."""
    db_circuit = Circuit.model_validate(circuit)
    session.add(db_circuit)
    session.commit()
    session.refresh(db_circuit)
    return db_circuit


@router.put("/circuits/{circuit_id}", response_model=CircuitRead)
def update_circuit(
    circuit_id: int,
    circuit: CircuitUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> Circuit:
    """Update a circuit."""
    db_circuit = session.get(Circuit, circuit_id)
    if not db_circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")

    circuit_data = circuit.model_dump(exclude_unset=True)
    for key, value in circuit_data.items():
        setattr(db_circuit, key, value)

    session.add(db_circuit)
    session.commit()
    session.refresh(db_circuit)
    return db_circuit


@router.delete("/circuits/{circuit_id}")
def delete_circuit(
    circuit_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Delete a circuit."""
    circuit = session.get(Circuit, circuit_id)
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")

    session.delete(circuit)
    session.commit()
    return {"message": "Circuit deleted successfully"}


@router.get("/circuits/search/{country}", response_model=list[CircuitRead])
def get_circuits_by_country(
    country: str,
    session: Annotated[Session, Depends(get_session)],
) -> list[Circuit]:
    """Get circuits by country (case-insensitive)."""
    statement = select(Circuit).where(
        func.lower(Circuit.country) == func.lower(country),
    )
    return list(session.exec(statement).all())


@router.get("/circuits/search/name/{name}", response_model=list[CircuitRead])
def search_circuits_by_name(
    name: str,
    session: Annotated[Session, Depends(get_session)],
) -> list[Circuit]:
    """Search circuits by name (case-insensitive partial match)."""
    statement = select(Circuit).where(
        func.lower(Circuit.name).like(f"%{name.lower()}%"),
    )
    return list(session.exec(statement).all())
