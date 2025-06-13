from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import create_db_and_tables
from src.routers import (
    circuits,
    constructors,
    drivers,
    qualifying,
    races,
    results,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan manager."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (add any cleanup code here if needed)


app = FastAPI(
    title="Formula 1 API",
    description=(
        "A comprehensive API for Formula 1 racing data with full CRUD "
        "operations"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(drivers.router, prefix="/api/v1", tags=["drivers"])
app.include_router(circuits.router, prefix="/api/v1", tags=["circuits"])
app.include_router(races.router, prefix="/api/v1", tags=["races"])
app.include_router(
    constructors.router,
    prefix="/api/v1",
    tags=["constructors"],
)
app.include_router(results.router, prefix="/api/v1", tags=["results"])
app.include_router(qualifying.router, prefix="/api/v1", tags=["qualifying"])


@app.get("/")
async def root() -> dict[str, str]:
    """Get API information."""
    return {
        "message": "Welcome to the Formula 1 API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "F1 API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
