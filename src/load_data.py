"""Data loader to populate the database with CSV data."""

import sys
from datetime import UTC, date, datetime
from datetime import time as time_type

import polars as pl
from sqlmodel import Session

sys.path.append("..")  # Ensure src is in the path for imports

from src.database import create_db_and_tables, engine
from src.models import Circuit, Constructor, Driver, Qualifying, Race, Result


def safe_date_parse(date_str: str | None) -> date | None:
    """Safely parse date string."""
    if not date_str or date_str == "\\N":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").astimezone(UTC)
    except (ValueError, TypeError):
        return None


def safe_time_parse(time_str: str | None) -> time_type | None:
    """Safely parse time string."""
    if not time_str or time_str == "\\N":
        return None
    try:
        return datetime.strptime(time_str, "%H:%M:%S").astimezone(UTC).time()
    except (ValueError, TypeError):
        return None


def load_csv_data() -> None:
    """Load data from CSV files into the database."""
    print("Loading data from CSV files...")

    create_db_and_tables()
    with Session(engine) as session:
        # Load drivers
        print("Loading drivers...")
        drivers_df = pl.read_csv("data/drivers.csv", null_values=["\\N"])

        for row in drivers_df.iter_rows(named=True):
            driver = Driver(
                driver_id=row["driverId"],
                driver_ref=row["driverRef"],
                number=row["number"],
                code=row["code"],
                forename=row["forename"],
                surname=row["surname"],
                dob=safe_date_parse(row["dob"]),
                nationality=row["nationality"],
                url=row["url"],
            )
            session.merge(driver)

        # Load circuits
        print("Loading circuits...")
        circuits_df = pl.read_csv("data/circuits.csv", null_values=["\\N"])

        for row in circuits_df.iter_rows(named=True):
            circuit = Circuit(
                circuit_id=row["circuitId"],
                circuit_ref=row["circuitRef"],
                name=row["name"],
                location=row["location"],
                country=row["country"],
                lat=row["lat"],
                lng=row["lng"],
                alt=row["alt"],
                url=row["url"],
            )
            session.merge(circuit)

        # Load constructors
        print("Loading constructors...")
        constructors_df = pl.read_csv(
            "data/constructors.csv",
            null_values=["\\N"],
        )

        for row in constructors_df.iter_rows(named=True):
            constructor = Constructor(
                constructor_id=row["constructorId"],
                constructor_ref=row["constructorRef"],
                name=row["name"],
                nationality=row["nationality"],
                url=row["url"],
            )
            session.merge(constructor)

        # Load races
        print("Loading races...")
        races_df = pl.read_csv("data/races.csv", null_values=["\\N"])

        for row in races_df.iter_rows(named=True):
            race = Race(
                race_id=row["raceId"],
                year=row["year"],
                round=row["round"],
                circuit_id=row["circuitId"],
                name=row["name"],
                date=safe_date_parse(row["date"]),
                time=safe_time_parse(row["time"]),
                url=row["url"],
                fp1_date=safe_date_parse(row["fp1_date"]),
                fp1_time=safe_time_parse(row["fp1_time"]),
                fp2_date=safe_date_parse(row["fp2_date"]),
                fp2_time=safe_time_parse(row["fp2_time"]),
                fp3_date=safe_date_parse(row["fp3_date"]),
                fp3_time=safe_time_parse(row["fp3_time"]),
                quali_date=safe_date_parse(row["quali_date"]),
                quali_time=safe_time_parse(row["quali_time"]),
                sprint_date=safe_date_parse(row["sprint_date"]),
                sprint_time=safe_time_parse(row["sprint_time"]),
            )
            session.merge(race)

        # Load results (sample first 1000 for performance)
        print("Loading results...")
        results_df = pl.read_csv(
            "data/results.csv",
            null_values=["\\N"],
            infer_schema_length=None,
        )

        for row in results_df.iter_rows(named=True):
            result = Result(
                result_id=row["resultId"],
                race_id=row["raceId"],
                driver_id=row["driverId"],
                constructor_id=row["constructorId"],
                number=row["number"],
                grid=row["grid"],
                position=row["position"],
                position_text=row["positionText"],
                position_order=row["positionOrder"],
                points=row["points"],
                laps=row["laps"],
                time=row["time"],
                milliseconds=row["milliseconds"],
                fastest_lap=row["fastestLap"],
                rank=row["rank"],
                fastest_lap_time=row["fastestLapTime"],
                fastest_lap_speed=row["fastestLapSpeed"],
                status_id=row["statusId"],
            )
            session.merge(result)

        # Load qualifying (sample first 1000 for performance)
        print("Loading qualifying...")
        qualifying_df = pl.read_csv(
            "data/qualifying.csv",
            null_values=["\\N"],
        )

        for row in qualifying_df.iter_rows(named=True):
            qualifying = Qualifying(
                qualify_id=row["qualifyId"],
                race_id=row["raceId"],
                driver_id=row["driverId"],
                constructor_id=row["constructorId"],
                number=row["number"],
                position=row["position"],
                q1=row["q1"],
                q2=row["q2"],
                q3=row["q3"],
            )
            session.merge(qualifying)

        session.commit()
        print("Data loading completed!")


if __name__ == "__main__":
    load_csv_data()
