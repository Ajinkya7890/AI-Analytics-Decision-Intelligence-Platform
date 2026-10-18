from __future__ import annotations

import collections
import datetime
import logging
import threading
import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas import (
    HealthResponse,
    HistoryEntry,
    HistoryResponse,
    QueryRequest,
    QueryResponse,
    serialize_rows,
    serialize_statistics,
)
from src.ai.query_pipeline import run_question
from src.config.database import get_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# In-memory thread-safe query history store (maximum 100 items, newest first)
_history_lock = threading.Lock()
_query_history: collections.deque[HistoryEntry] = collections.deque(maxlen=100)


def record_history(
    question: str,
    success: bool,
    row_count: int | None = None,
    execution_time_ms: float | None = None,
    error_message: str | None = None,
) -> HistoryEntry:
    """
    Thread-safely record a query execution in the in-memory history ring buffer.
    """
    entry = HistoryEntry(
        id=str(uuid.uuid4()),
        question=question,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        success=success,
        row_count=row_count,
        execution_time_ms=execution_time_ms,
        error_message=error_message,
    )
    with _history_lock:
        # Append to the left so index 0 is always newest
        _query_history.appendleft(entry)
    return entry


def clear_history() -> None:
    """
    Helper to clear history (used primarily for test isolation).
    """
    with _history_lock:
        _query_history.clear()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API and database health status",
    description="Returns the status of the API and checks active PostgreSQL connectivity without exposing credentials."
)
def get_health() -> HealthResponse:
    """
    Check API and PostgreSQL connectivity independently of any external LLM service.
    """
    db_status = "disconnected"
    service_status = "degraded"

    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()
                db_status = "connected"
                service_status = "healthy"
        finally:
            connection.close()
    except Exception as exc:
        logger.error(f"Health check database connection error: {exc}")
        db_status = "disconnected"
        service_status = "degraded"

    return HealthResponse(
        status=service_status,
        database=db_status,
        version="1.0.0",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Execute a natural-language analytical query",
    description="Executes a business question through the deterministic SQL analytics pipeline and PostgreSQL."
)
def execute_query_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Execute natural-language question through the existing analytics pipeline.
    """
    start_time = time.perf_counter()

    try:
        result = run_question(request.question)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        columns = result.get("columns", [])
        raw_rows = result.get("rows", [])
        serialized_rows = serialize_rows(raw_rows)
        serialized_stats = serialize_statistics(result.get("statistics"))

        plan = result.get("plan", {})
        intent = plan.get("intent")
        target_entity = plan.get("target_entity")
        metrics = plan.get("metrics")
        dimensions = plan.get("dimensions")
        sql = result.get("sql", "")
        validation = result.get("validation")

        # Record successful query in history
        record_history(
            question=request.question,
            success=True,
            row_count=len(serialized_rows),
            execution_time_ms=duration_ms,
        )

        return QueryResponse(
            question=request.question,
            success=True,
            sql=sql,
            columns=columns,
            rows=serialized_rows,
            row_count=len(serialized_rows),
            statistics=serialized_stats,
            execution_time_ms=duration_ms,
            intent=intent,
            target_entity=target_entity,
            metrics=metrics,
            dimensions=dimensions,
            validation=validation,
        )

    except ValueError as exc:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        err_msg = str(exc)
        logger.warning(f"Pipeline validation error for query '{request.question}': {err_msg}")

        # Record validation failure in history
        record_history(
            question=request.question,
            success=False,
            execution_time_ms=duration_ms,
            error_message=err_msg,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg,
        )

    except Exception as exc:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error(f"Internal execution error for query '{request.question}': {exc}", exc_info=True)

        # Record unexpected error in history with a safe description
        record_history(
            question=request.question,
            success=False,
            execution_time_ms=duration_ms,
            error_message="Analytical query execution error",
        )

        # Return a safe error message without internal credentials or stack traces
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while executing the analytical query.",
        )


@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Get recent query execution history",
    description="Returns in-memory history of recent queries executed in the current session (maximum 100 entries, newest first)."
)
def get_query_history() -> HistoryResponse:
    """
    Return recent query execution history (newest first).
    """
    with _history_lock:
        entries = list(_query_history)

    return HistoryResponse(
        total=len(entries),
        entries=entries,
    )
