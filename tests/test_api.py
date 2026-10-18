from __future__ import annotations

import concurrent.futures
import datetime
from decimal import Decimal
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import clear_history, record_history, _query_history
from app.schemas import serialize_rows, serialize_statistics, serialize_value

client = TestClient(app)


class TestApiBackend(unittest.TestCase):

    def setUp(self):
        clear_history()

    # 1. Health endpoint returns expected structure
    def test_health_endpoint_structure(self):
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("database", data)
        self.assertIn("version", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["database"], "connected")
        self.assertEqual(data["status"], "healthy")

    # 2. PostgreSQL connectivity is checked independently of Ollama
    @patch("app.api.routes.get_connection")
    def test_health_endpoint_degraded_when_db_down(self, mock_get_conn):
        mock_get_conn.side_effect = Exception("Connection to database failed: host unreachable")
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "degraded")
        self.assertEqual(data["database"], "disconnected")
        # Ensure error message/connection details are NOT leaked to response
        self.assertNotIn("Connection to database failed", str(data))

    # 3. Valid natural-language question returns correctly structured response
    def test_query_endpoint_real_pipeline(self):
        question = "Which categories generated the highest revenue?"
        response = client.post("/api/query", json={"question": question})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["question"], question)
        self.assertTrue(data["success"])
        self.assertIn("category_name_english", data["columns"])
        self.assertIn("total_revenue", data["columns"])
        self.assertIsInstance(data["rows"], list)
        self.assertGreater(len(data["rows"]), 0)
        self.assertEqual(data["row_count"], len(data["rows"]))
        self.assertIsInstance(data["execution_time_ms"], (int, float))
        self.assertGreater(data["execution_time_ms"], 0)
        # Verify first row data type: first element string (category), second element float (revenue)
        first_row = data["rows"][0]
        self.assertEqual(first_row[0], "health_beauty")
        self.assertIsInstance(first_row[1], (int, float))
        self.assertEqual(first_row[1], 1258681.34)

    # 4. Empty, whitespace-only, and invalid questions are rejected
    def test_query_validation_rejects_empty_and_whitespace(self):
        # Empty string
        resp1 = client.post("/api/query", json={"question": ""})
        self.assertEqual(resp1.status_code, 422)

        # Whitespace-only string
        resp2 = client.post("/api/query", json={"question": "   \n\t  "})
        self.assertEqual(resp2.status_code, 422)

        # Non-string question
        resp3 = client.post("/api/query", json={"question": 12345})
        self.assertEqual(resp3.status_code, 422)

        # Missing question field
        resp4 = client.post("/api/query", json={})
        self.assertEqual(resp4.status_code, 422)

        # Excessively long question (> 1000 chars)
        long_q = "What is the revenue? " * 100
        resp5 = client.post("/api/query", json={"question": long_q})
        self.assertEqual(resp5.status_code, 422)

    # 5. Serialization of Decimal, date, and datetime types
    def test_serialization_helpers(self):
        test_rows = [
            ("electronics", Decimal("1234.56"), datetime.date(2017, 5, 1)),
            ("furniture", Decimal("100.00"), datetime.datetime(2018, 1, 1, 12, 0, 0)),
            ("toys", None, float("nan"))
        ]
        serialized = serialize_rows(test_rows)
        # Decimal("1234.56") -> 1234.56 (float)
        self.assertEqual(serialized[0][1], 1234.56)
        # Date -> "2017-05-01" (ISO string)
        self.assertEqual(serialized[0][2], "2017-05-01")
        # Decimal("100.00") -> 100 (int)
        self.assertEqual(serialized[1][1], 100)
        # Datetime -> "2018-01-01T12:00:00"
        self.assertEqual(serialized[1][2], "2018-01-01T12:00:00")
        # None -> None
        self.assertIsNone(serialized[2][1])
        # NaN -> None
        self.assertIsNone(serialized[2][2])

        # Test statistics serialization
        stats = {
            "mean": Decimal("45.67"),
            "count": 10,
            "std": float("nan")
        }
        serialized_stats = serialize_statistics(stats)
        self.assertEqual(serialized_stats["mean"], 45.67)
        self.assertEqual(serialized_stats["count"], 10)
        self.assertIsNone(serialized_stats["std"])

    # 6. Pipeline exception returns safe error response
    @patch("app.api.routes.run_question")
    def test_pipeline_exception_handling(self, mock_run):
        # ValueError from analytical planning / validation
        mock_run.side_effect = ValueError("Unsupported metric request: UnknownMetric")
        resp = client.post("/api/query", json={"question": "What is the unknown metric?"})
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertEqual(data["detail"], "Unsupported metric request: UnknownMetric")

        # Unexpected database error must not leak credentials or internal details
        mock_run.side_effect = Exception("psycopg2.OperationalError: password authentication failed for user 'secret'")
        resp_db = client.post("/api/query", json={"question": "Show revenue"})
        self.assertEqual(resp_db.status_code, 500)
        data_db = resp_db.json()
        self.assertEqual(data_db["detail"], "An internal error occurred while executing the analytical query.")
        self.assertNotIn("secret", str(data_db))
        self.assertNotIn("OperationalError", str(data_db))

    # 7. Successful and failed queries appear correctly in history
    def test_history_records_success_and_failure(self):
        # 1. Successful query
        client.post("/api/query", json={"question": "Which categories generated the highest revenue?"})

        # 2. Failed query (bad request)
        with patch("app.api.routes.run_question", side_effect=ValueError("Invalid plan")):
            client.post("/api/query", json={"question": "Invalid question that fails plan"})

        resp = client.get("/api/history")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 2)
        # Newest first: the failed query was executed last, so it should be at index 0
        self.assertEqual(data["entries"][0]["question"], "Invalid question that fails plan")
        self.assertFalse(data["entries"][0]["success"])
        self.assertEqual(data["entries"][0]["error_message"], "Invalid plan")

        # The successful query should be at index 1
        self.assertEqual(data["entries"][1]["question"], "Which categories generated the highest revenue?")
        self.assertTrue(data["entries"][1]["success"])
        self.assertEqual(data["entries"][1]["row_count"], 10)

    # 8. History is capped at 100 entries and returned newest-first
    def test_history_capped_at_100_entries(self):
        for i in range(120):
            record_history(question=f"Question number {i}", success=True, row_count=i)

        resp = client.get("/api/history")
        data = resp.json()
        self.assertEqual(data["total"], 100)
        self.assertEqual(len(data["entries"]), 100)
        # Newest item was question 119
        self.assertEqual(data["entries"][0]["question"], "Question number 119")
        # Oldest item remaining should be question 20
        self.assertEqual(data["entries"][-1]["question"], "Question number 20")

    # 9. Concurrent history additions do not corrupt history
    def test_concurrent_history_recording(self):
        clear_history()

        def add_entries(thread_id):
            for i in range(25):
                record_history(
                    question=f"Thread {thread_id} - Question {i}",
                    success=True,
                    row_count=i
                )

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(add_entries, t) for t in range(8)]
            concurrent.futures.wait(futures)

        resp = client.get("/api/history")
        data = resp.json()
        # 8 threads * 25 queries = 200 additions, capped at maxlen=100
        self.assertEqual(data["total"], 100)
        self.assertEqual(len(data["entries"]), 100)

    # 10. SQL validation safeguards are active in pipeline
    def test_sql_validator_safeguard(self):
        # Attempting a question that generates forbidden SQL or causes multiple statements
        with patch("app.api.routes.run_question", side_effect=ValueError("Forbidden SQL operation detected: DROP")):
            resp = client.post("/api/query", json={"question": "Drop database orders"})
            self.assertEqual(resp.status_code, 400)
            self.assertIn("Forbidden SQL operation detected: DROP", resp.json()["detail"])

    # 11. No endpoint allows arbitrary user-supplied SQL execution
    def test_no_arbitrary_sql_endpoint_exists(self):
        # Attempting to POST raw SQL to /api/sql or /api/execute must return 404 Not Found
        resp_sql = client.post("/api/sql", json={"sql": "SELECT * FROM core.dim_customer;"})
        self.assertEqual(resp_sql.status_code, 404)

        resp_exec = client.post("/api/execute", json={"sql": "SELECT 1;"})
        self.assertEqual(resp_exec.status_code, 404)


if __name__ == "__main__":
    unittest.main()
