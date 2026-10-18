from __future__ import annotations

import datetime
from decimal import Decimal
import math
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


def serialize_value(val: Any) -> Any:
    """
    Safely serialize database and analytical Python types into JSON-compatible values.
    """
    if val is None:
        return None
    if isinstance(val, Decimal):
        # Convert Decimal to int if exact integer, else float
        if val % 1 == 0:
            return int(val)
        return float(val)
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.isoformat()
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
        return val
    if isinstance(val, (int, str, bool)):
        return val
    return str(val)


def serialize_rows(rows: list[Any]) -> list[list[Any]]:
    """
    Serialize query row tuples into JSON-compatible lists of values.
    """
    return [[serialize_value(item) for item in row] for row in rows]


def serialize_statistics(stats: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    """
    Serialize descriptive statistics values into JSON-compatible values.
    """
    if not stats:
        return None
    return {k: serialize_value(v) for k, v in stats.items()}


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall API service health status")
    database: str = Field(..., description="PostgreSQL database connectivity status")
    version: str = Field(default="1.0.0", description="API version")
    timestamp: str = Field(..., description="Current UTC timestamp in ISO 8601 format")


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Natural-language business question",
        min_length=2,
        max_length=1000
    )

    @field_validator("question")
    @classmethod
    def validate_non_empty_question(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Question cannot be empty or contain only whitespace.")
        return stripped


class QueryResponse(BaseModel):
    question: str
    success: bool
    sql: str
    columns: list[str]
    rows: list[list[Any]]
    row_count: int
    statistics: Optional[dict[str, Any]] = None
    execution_time_ms: float
    intent: Optional[str] = None
    target_entity: Optional[str] = None
    metrics: Optional[list[str]] = None
    dimensions: Optional[list[str]] = None
    validation: Optional[str] = None


class HistoryEntry(BaseModel):
    id: str
    question: str
    timestamp: str
    success: bool
    row_count: Optional[int] = None
    execution_time_ms: Optional[float] = None
    error_message: Optional[str] = None


class HistoryResponse(BaseModel):
    total: int
    entries: list[HistoryEntry]
