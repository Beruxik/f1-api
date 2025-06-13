from datetime import date as date_type
from datetime import time as time_type

from sqlmodel import Field, SQLModel


class DriverBase(SQLModel):
    """Base model for Driver."""

    driver_ref: str = Field(index=True)
    number: int | None = None
    code: str | None = None
    forename: str
    surname: str
    dob: date_type | None = None
    nationality: str
    url: str | None = None


class Driver(DriverBase, table=True):
    """Driver table model."""

    driver_id: int | None = Field(default=None, primary_key=True)


class DriverCreate(DriverBase):
    """Model for creating a new driver."""


class DriverRead(DriverBase):
    """Model for reading driver data."""

    driver_id: int


class DriverUpdate(SQLModel):
    """Model for updating driver data."""

    driver_ref: str | None = None
    number: int | None = None
    code: str | None = None
    forename: str | None = None
    surname: str | None = None
    dob: date_type | None = None
    nationality: str | None = None
    url: str | None = None


class CircuitBase(SQLModel):
    """Base model for Circuit."""

    circuit_ref: str = Field(index=True)
    name: str
    location: str
    country: str
    lat: float | None = None
    lng: float | None = None
    alt: int | None = None
    url: str | None = None


class Circuit(CircuitBase, table=True):
    """Circuit table model."""

    circuit_id: int | None = Field(default=None, primary_key=True)


class CircuitCreate(CircuitBase):
    """Model for creating a new circuit."""


class CircuitRead(CircuitBase):
    """Model for reading circuit data."""

    circuit_id: int


class CircuitUpdate(SQLModel):
    """Model for updating circuit data."""

    circuit_ref: str | None = None
    name: str | None = None
    location: str | None = None
    country: str | None = None
    lat: float | None = None
    lng: float | None = None
    alt: int | None = None
    url: str | None = None


class ConstructorBase(SQLModel):
    """Base model for Constructor."""

    constructor_ref: str = Field(index=True)
    name: str
    nationality: str
    url: str | None = None


class Constructor(ConstructorBase, table=True):
    """Constructor table model."""

    constructor_id: int | None = Field(default=None, primary_key=True)


class ConstructorCreate(ConstructorBase):
    """Model for creating a new constructor."""


class ConstructorRead(ConstructorBase):
    """Model for reading constructor data."""

    constructor_id: int


class ConstructorUpdate(SQLModel):
    """Model for updating constructor data."""

    constructor_ref: str | None = None
    name: str | None = None
    nationality: str | None = None
    url: str | None = None


class RaceBase(SQLModel):
    """Base model for Race."""

    year: int = Field(index=True)
    round: int
    circuit_id: int = Field(foreign_key="circuit.circuit_id")
    name: str
    date: date_type | None = None
    time: time_type | None = None
    url: str | None = None
    fp1_date: date_type | None = None
    fp1_time: time_type | None = None
    fp2_date: date_type | None = None
    fp2_time: time_type | None = None
    fp3_date: date_type | None = None
    fp3_time: time_type | None = None
    quali_date: date_type | None = None
    quali_time: time_type | None = None
    sprint_date: date_type | None = None
    sprint_time: time_type | None = None


class Race(RaceBase, table=True):
    """Race table model."""

    race_id: int | None = Field(default=None, primary_key=True)


class RaceCreate(RaceBase):
    """Model for creating a new race."""


class RaceRead(RaceBase):
    """Model for reading race data."""

    race_id: int


class RaceUpdate(SQLModel):
    """Model for updating race data."""

    year: int | None = None
    round: int | None = None
    circuit_id: int | None = None
    name: str | None = None
    date: date_type | None = None
    time: time_type | None = None
    url: str | None = None
    fp1_date: date_type | None = None
    fp1_time: time_type | None = None
    fp2_date: date_type | None = None
    fp2_time: time_type | None = None
    fp3_date: date_type | None = None
    fp3_time: time_type | None = None
    quali_date: date_type | None = None
    quali_time: time_type | None = None
    sprint_date: date_type | None = None
    sprint_time: time_type | None = None


class ResultBase(SQLModel):
    """Base model for Result."""

    race_id: int = Field(foreign_key="race.race_id")
    driver_id: int = Field(foreign_key="driver.driver_id")
    constructor_id: int = Field(foreign_key="constructor.constructor_id")
    number: int | None = None
    grid: int | None = None
    position: int | None = None
    position_text: str
    position_order: int
    points: float
    laps: int
    time: str | None = None
    milliseconds: int | None = None
    fastest_lap: int | None = None
    rank: int | None = None
    fastest_lap_time: str | None = None
    fastest_lap_speed: str | None = None
    status_id: int


class Result(ResultBase, table=True):
    """Result table model."""

    result_id: int | None = Field(default=None, primary_key=True)


class ResultCreate(ResultBase):
    """Model for creating a new result."""


class ResultRead(ResultBase):
    """Model for reading result data."""

    result_id: int


class ResultUpdate(SQLModel):
    """Model for updating result data."""

    race_id: int | None = None
    driver_id: int | None = None
    constructor_id: int | None = None
    number: int | None = None
    grid: int | None = None
    position: int | None = None
    position_text: str | None = None
    position_order: int | None = None
    points: float | None = None
    laps: int | None = None
    time: str | None = None
    milliseconds: int | None = None
    fastest_lap: int | None = None
    rank: int | None = None
    fastest_lap_time: str | None = None
    fastest_lap_speed: str | None = None
    status_id: int | None = None


class QualifyingBase(SQLModel):
    """Base model for Qualifying."""

    race_id: int = Field(foreign_key="race.race_id")
    driver_id: int = Field(foreign_key="driver.driver_id")
    constructor_id: int = Field(foreign_key="constructor.constructor_id")
    number: int
    position: int | None = None
    q1: str | None = None
    q2: str | None = None
    q3: str | None = None


class Qualifying(QualifyingBase, table=True):
    """Qualifying table model."""

    qualify_id: int | None = Field(default=None, primary_key=True)


class QualifyingCreate(QualifyingBase):
    """Model for creating a new qualifying result."""


class QualifyingRead(QualifyingBase):
    """Model for reading qualifying data."""

    qualify_id: int


class QualifyingUpdate(SQLModel):
    """Model for updating qualifying data."""

    race_id: int | None = None
    driver_id: int | None = None
    constructor_id: int | None = None
    number: int | None = None
    position: int | None = None
    q1: str | None = None
    q2: str | None = None
    q3: str | None = None
