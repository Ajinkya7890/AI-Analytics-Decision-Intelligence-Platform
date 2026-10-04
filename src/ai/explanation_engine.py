class ExplanationEngine:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def build_prompt(self, question, investigation_report):

        report = investigation_report

        period = report["period"]
        overall = report["overall"]

        previous_year = period["previous_year"]
        current_year = period["current_year"]

        previous_revenue = overall["previous_revenue"]
        current_revenue = overall["current_revenue"]
        revenue_change = overall["revenue_change"]
        percentage_change = overall["percentage_change"]

        if revenue_change > 0:
            overall_direction = "increased"
        elif revenue_change < 0:
            overall_direction = "decreased"
        else:
            overall_direction = "remained unchanged"

        prompt = f"""
You are an analytical business intelligence assistant.

Answer the user's business question using ONLY the
structured analytical report provided below.

USER QUESTION:
{question}

ANALYTICAL REPORT
=================

ANALYSIS PERIOD:
{previous_year} to {current_year}

OVERALL RESULT:
Previous revenue: {previous_revenue:,.2f}
Current revenue: {current_revenue:,.2f}
Revenue change: {revenue_change:,.2f}
Percentage change: {percentage_change:.2f}%
Overall revenue direction: {overall_direction}

IMPORTANT BUSINESS SEMANTICS
=============================

The overall revenue direction above is authoritative.

A category can decline even when total company revenue increases.

Therefore:

- A declining category is a negative contributor to overall
  revenue growth.
- A declining category is NOT evidence that overall revenue
  decreased unless the overall result explicitly says revenue
  decreased.
- A growing category is a positive contributor to overall
  revenue growth.
- A growth drag is a negative effect inside a category that
  still contributed positively overall.
- A decline offset is a positive effect inside a category that
  still contributed negatively overall.

Never confuse category-level movement with overall revenue direction.

TOP POSITIVE CONTRIBUTORS
=========================
"""

        for index, category in enumerate(
            report["top_positive_contributors"],
            start=1
        ):

            prompt += f"""
{index}. {category["category"]}

Revenue contribution:
{category["revenue_change"]:,.2f}

Share of total revenue change:
{category["contribution_pct"]:.2f}%

Primary growth driver:
{category["growth_driver"]} → {category["growth_driver_effect"]:,.2f}
"""

            if category["growth_drag"]:
                prompt += f"""
Growth drag within this growing category:
{category["growth_drag"]} → {category["growth_drag_effect"]:,.2f}
"""

        prompt += """

TOP NEGATIVE CONTRIBUTORS
=========================
"""

        for index, category in enumerate(
            report["top_negative_contributors"],
            start=1
        ):

            prompt += f"""
{index}. {category["category"]}

Revenue change:
{category["revenue_change"]:,.2f}

Share of total revenue change:
{category["contribution_pct"]:.2f}%

Primary decline driver:
{category["decline_driver"]} → {category["decline_driver_effect"]:,.2f}
"""

            if category["decline_offset"]:
                prompt += f"""
Decline offset within this declining category:
{category["decline_offset"]} → {category["decline_offset_effect"]:,.2f}
"""

        prompt += """

RESPONSE STRUCTURE
==================

1. OVERALL RESULT

State clearly whether overall revenue increased, decreased,
or remained unchanged.

Use the exact overall revenue change and percentage change.

If the user's question contains an incorrect assumption about
the overall direction, explicitly correct that assumption.

2. GROWTH CONTRIBUTORS

Explain the most important categories that contributed
positively to the overall revenue change.

Mention their revenue contribution and primary growth driver.

3. GROWTH DRAGS

Only mention a growth drag when it belongs to a category
that itself contributed positively.

Explain that the drag reduced the category's positive impact.

Do NOT describe a growth drag as an overall revenue decline.

4. DECLINING CATEGORIES

Explain categories whose revenue contribution was negative.

Use wording such as:

- "negative contributor to overall revenue growth"
- "reduced the overall revenue growth"
- "experienced a category-level decline"

Do NOT say that these categories caused overall revenue
to decrease when the overall result shows revenue growth.

5. DECLINE OFFSETS

Only mention an offset when it belongs to a declining category.

Explain that the offset partially reduced that category's
negative contribution.

Do NOT describe a decline offset as an overall growth driver.

6. BUSINESS INTERPRETATION

Summarize:

- overall revenue direction,
- magnitude of the change,
- strongest positive contributors,
- strongest negative contributors,
- primary drivers behind those movements.

Maintain a strict distinction between:

- overall revenue direction,
- positive contributors,
- negative contributors,
- growth drags,
- decline offsets.

RULES
=====

- Use ONLY the analytical report.
- Do not invent facts.
- Do not invent numbers.
- Do not calculate new metrics.
- Do not change numerical values.
- Do not contradict the overall revenue direction.
- Do not confuse category-level declines with overall decline.
- Do not describe negative contributors as causing an overall
  decrease when overall revenue increased.
- Preserve the analytical meaning of every driver.
- Keep the response concise and business-focused.
"""

        return prompt

    def explain(self, question, investigation_report):

        prompt = self.build_prompt(
            question=question,
            investigation_report=investigation_report
        )

        response = self.llm_client.generate(prompt)

        return {
            "question": question,
            "report": investigation_report,
            "prompt": prompt,
            "explanation": response
        }