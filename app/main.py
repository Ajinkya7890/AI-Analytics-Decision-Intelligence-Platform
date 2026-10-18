from __future__ import annotations

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_analytics_api")

app = FastAPI(
    title="AI Analytics & Decision Intelligence Platform API",
    description=(
        "Production-grade REST API exposing the natural-language analytics engine, "
        "deterministic SQL generation, validation, and PostgreSQL query execution."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS strictly for the local React + Vite frontend origin
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)


@app.get("/", summary="Root API metadata")
def root():
    """
    Return basic service metadata and documentation links.
    """
    return {
        "service": "AI Analytics & Decision Intelligence Platform API",
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
