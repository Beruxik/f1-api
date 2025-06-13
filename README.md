# Formula 1 API

A comprehensive FastAPI application for managing Formula 1 racing data with full CRUD operations.

## Authors

- **Jakub Rejdych**
- **Michał Rojczyk**

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete operations for all F1 entities
- **RESTful API**: Well-structured endpoints following REST principles
- **SQLModel Integration**: Type-safe database models with automatic OpenAPI schema generation
- **CSV Data Import**: Load existing F1 data from CSV files
- **Interactive Documentation**: Automatic API documentation with Swagger UI and ReDoc
- **Data Validation**: Pydantic models for request/response validation

## Entities

The API manages the following F1 entities:

- **Drivers**: F1 driver information (name, nationality, dates, etc.)
- **Circuits**: Racing circuit details (name, location, coordinates, etc.)
- **Constructors**: F1 teams and constructor information
- **Races**: Race details (season, circuit, dates, sessions)
- **Results**: Race results and performance data
- **Qualifying**: Qualifying session results

## Installation

### Prerequisites

1. **Download F1 Dataset**: Download the Formula 1 dataset from Kaggle:
   - Visit: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
   - Download the dataset (you'll need a Kaggle account)
   - Extract the CSV files to the `src/data/` folder in your project directory

   The `src/data/` folder should contain these CSV files:
   - `circuits.csv`
   - `drivers.csv`
   - `constructors.csv`
   - `races.csv`
   - `results.csv`
   - `qualifying.csv`
   - `constructor_results.csv`
   - `constructor_standings.csv`
   - `driver_standings.csv`
   - `lap_times.csv`
   - `pit_stops.csv`
   - `seasons.csv`
   - `sprint_results.csv`
   - `status.csv`

### Setup

1. Install dependencies using uv:
```bash
uv sync
```

2. (Optional) Load sample data from CSV files:
```bash
uv run python src/load_data.py
```

3. Run the application:
```bash
uv run fastapi run src/main.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Base URL
- Local development: `http://localhost:8000`
- API base path: `/api/v1`

### Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Core Endpoints

#### Drivers
- `GET /api/v1/drivers` - List all drivers (with pagination)
- `GET /api/v1/drivers/{driver_id}` - Get specific driver
- `POST /api/v1/drivers` - Create new driver
- `PUT /api/v1/drivers/{driver_id}` - Update driver
- `DELETE /api/v1/drivers/{driver_id}` - Delete driver
- `GET /api/v1/drivers/search/{nationality}` - Search drivers by nationality

#### Circuits
- `GET /api/v1/circuits` - List all circuits
- `GET /api/v1/circuits/{circuit_id}` - Get specific circuit
- `POST /api/v1/circuits` - Create new circuit
- `PUT /api/v1/circuits/{circuit_id}` - Update circuit
- `DELETE /api/v1/circuits/{circuit_id}` - Delete circuit
- `GET /api/v1/circuits/search/{country}` - Search circuits by country

#### Races
- `GET /api/v1/races` - List all races
- `GET /api/v1/races/{race_id}` - Get specific race
- `POST /api/v1/races` - Create new race
- `PUT /api/v1/races/{race_id}` - Update race
- `DELETE /api/v1/races/{race_id}` - Delete race
- `GET /api/v1/races/year/{year}` - Get races by year

#### Constructors
- `GET /api/v1/constructors` - List all constructors
- `GET /api/v1/constructors/{constructor_id}` - Get specific constructor
- `POST /api/v1/constructors` - Create new constructor
- `PUT /api/v1/constructors/{constructor_id}` - Update constructor
- `DELETE /api/v1/constructors/{constructor_id}` - Delete constructor
- `GET /api/v1/constructors/search/{nationality}` - Search constructors by nationality

#### Results
- `GET /api/v1/results` - List all results
- `GET /api/v1/results/{result_id}` - Get specific result
- `POST /api/v1/results` - Create new result
- `PUT /api/v1/results/{result_id}` - Update result
- `DELETE /api/v1/results/{result_id}` - Delete result
- `GET /api/v1/results/race/{race_id}` - Get results by race
- `GET /api/v1/results/driver/{driver_id}` - Get results by driver

#### Qualifying
- `GET /api/v1/qualifying` - List all qualifying results
- `GET /api/v1/qualifying/{qualify_id}` - Get specific qualifying result
- `POST /api/v1/qualifying` - Create new qualifying result
- `PUT /api/v1/qualifying/{qualify_id}` - Update qualifying result
- `DELETE /api/v1/qualifying/{qualify_id}` - Delete qualifying result
- `GET /api/v1/qualifying/race/{race_id}` - Get qualifying results by race

## Example Usage

### Create a new driver
```bash
curl -X POST "http://localhost:8000/api/v1/drivers" \
  -H "Content-Type: application/json" \
  -d '{
    "driver_ref": "verstappen",
    "number": 1,
    "code": "VER",
    "forename": "Max",
    "surname": "Verstappen",
    "dob": "1997-09-30",
    "nationality": "Dutch",
    "url": "http://en.wikipedia.org/wiki/Max_Verstappen"
  }'
```

### Get all drivers
```bash
curl "http://localhost:8000/api/v1/drivers"
```

### Search drivers by nationality
```bash
curl "http://localhost:8000/api/v1/drivers/search/Dutch"
```

## Database

The application uses SQLite by default with SQLModel for ORM. The database file `f1_data.db` will be created automatically in the project root.

You can change the database URL by setting the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost/f1_db"
```

## Development

The application is built with:
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: SQL databases with Python types (built on SQLAlchemy and Pydantic)
- **Polars**: Fast DataFrames library for data manipulation and CSV loading
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
src/
├── data/           # CSV data files
├── routers/        # API route handlers
│   ├── drivers.py
│   ├── circuits.py
│   ├── races.py
│   ├── constructors.py
│   ├── results.py
│   └── qualifying.py
├── database.py     # Database configuration
├── models.py       # SQLModel database models
├── main.py         # FastAPI application
└── load_data.py    # CSV data loader utility
```

## Data Source

This project uses the Formula 1 World Championship dataset (1950-2020) from Kaggle:
- **Dataset**: [Formula 1 World Championship (1950 - 2020)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
- **Author**: Rohan Rao
- **License**: Please refer to the Kaggle dataset page for licensing information

The dataset contains comprehensive F1 data including race results, driver information, circuit details, constructor data, and more spanning from 1950 to 2020.

## License

This project is licensed under the MIT License.