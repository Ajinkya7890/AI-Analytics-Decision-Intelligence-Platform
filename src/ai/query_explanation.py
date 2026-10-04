from src.ai.query_evidence_formatter import format_evidence


class QueryExplanationEngine:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def build_prompt(
        self,
        question,
        plan,
        columns,
        rows,
        statistics=None
    ):
        evidence = format_evidence(
            columns=columns,
            rows=rows,
            statistics=statistics
        )

        dimensions = plan.get("dimensions", [])
        metrics = plan.get("metrics", [])
        operations = plan.get("operations", [])

        prompt = f"""
You are a business analytics assistant.

Answer the user's business question using ONLY the
analytical evidence provided below.

USER QUESTION:
{question}

ANALYTICAL PLAN
===============

Intent:
{plan["intent"]}

Metrics:
{metrics}

Dimensions:
{dimensions}

Operations:
{operations}

Source Tables:
{plan["source_tables"]}

Grouping:
{plan["group_by"]}

Sorting:
{plan["sorting"]}

RESULT INTERPRETATION
=====================

The result rows represent observations at the
analytical grain requested by the question.

Detected analytical dimensions:
{dimensions}

Detected metrics:
{metrics}

Interpret each result column according to its
column name and the analytical plan.

Do NOT treat a descriptive dimension column as
the metric being measured.

For example, when the dimension is Product and
the metric is Revenue:

- product_id identifies the product.
- category_name_english identifies the category
  associated with that product.
- total_revenue represents the revenue generated
  by that individual product.

The category column must NOT be interpreted as
the revenue value itself.

STATISTICAL EVIDENCE
====================

If statistical analysis is provided, treat it as
verified evidence calculated by the analytical
system.

Do not recalculate statistical values yourself.

ANALYTICAL EVIDENCE
===================

{evidence}

RESPONSE RULES:

- Answer the user's question directly.
- Use ONLY the analytical evidence above.
- Do not invent facts, numbers, categories, or explanations.
- Do not calculate new metrics.
- Do not perform additional analysis that is not represented
  by the provided evidence.
- Preserve the exact values from the evidence.
- Respect the analytical grain of each row.
- Distinguish dimensions from metrics.
- If statistical evidence is provided, use those values
  directly.
- If the results are ranked, explain the ranking using
  the metric column and supplied ordering.
- If the evidence is insufficient to answer the question,
  explicitly say so.
- Keep the response concise and business-focused.
"""

        return prompt

    def explain(
        self,
        question,
        plan,
        columns,
        rows,
        statistics=None
    ):
        prompt = self.build_prompt(
            question=question,
            plan=plan,
            columns=columns,
            rows=rows,
            statistics=statistics
        )

        response = self.llm_client.generate(prompt)

        return {
            "question": question,
            "plan": plan,
            "columns": columns,
            "rows": rows,
            "statistics": statistics,
            "prompt": prompt,
            "explanation": response
        }