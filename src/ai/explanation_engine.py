class ExplanationEngine:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def build_prompt(self, question, investigation_report):

        report = investigation_report

        previous_year, current_year = report["period"]
        overall = report["overall_result"]

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
Previous revenue: ₹{overall["previous_revenue"]:,.2f}
Current revenue: ₹{overall["current_revenue"]:,.2f}
Revenue change: ₹{overall["revenue_change"]:,.2f}
Percentage change: {overall["percentage_change"]:.2f}%

TOP GROWTH CONTRIBUTORS:
"""

        for index, driver in enumerate(
            report["growth_drivers"],
            start=1
        ):
            prompt += f"""
{index}. {driver["category"]}
Revenue contribution: ₹{driver["revenue_change"]:,.2f}
Share of total revenue change: {driver["contribution_pct"]:.2f}%

Growth driver:
{driver["primary_driver"]} → ₹{driver["primary_driver_effect"]:,.2f}
"""

            if driver["primary_drag"]:
                prompt += f"""
Growth drag within this growing category:
{driver["primary_drag"]} → ₹{driver["primary_drag_effect"]:,.2f}
"""

        prompt += """

TOP DECLINING CATEGORIES:
"""

        for index, category in enumerate(
            report["declining_categories"],
            start=1
        ):
            prompt += f"""
{index}. {category["category"]}
Revenue change: ₹{category["revenue_change"]:,.2f}
Share of total revenue change: {category["contribution_pct"]:.2f}%

Decline driver:
{category["primary_driver"]} → ₹{category["primary_driver_effect"]:,.2f}
"""

            if category["offset"]:
                prompt += f"""
Decline offset within this declining category:
{category["offset"]} → ₹{category["offset_effect"]:,.2f}
"""

        prompt += """

RESPONSE STRUCTURE:

1. OVERALL RESULT
State whether revenue increased or decreased.
If the user's question contains an incorrect assumption,
correct it explicitly.

2. GROWTH DRIVERS
Explain the most important categories that increased revenue.
For each category, mention its revenue contribution and
primary growth driver.

3. GROWTH DRAGS
Only mention a growth drag when it belongs to a category
that itself contributed positively to revenue.
A growth drag is a negative effect within a growing category.
It must NOT be described as an overall revenue decline.

4. DECLINING CATEGORIES
Explain the most important categories that reduced revenue.
For each category, mention its revenue decline and primary
decline driver.

5. DECLINE OFFSETS
Only mention an offset when it belongs to a declining category.
An offset partially reduces that category's decline.
It must NOT be described as an overall revenue growth driver.

6. BUSINESS INTERPRETATION
Summarize ONLY:
- the overall revenue direction and magnitude,
- the most important positive contributors and their drivers,
- the most important negative contributors and their drivers.

Do NOT use decline offsets as evidence of overall revenue growth.
Do NOT use growth drags as evidence of overall revenue decline.
Do NOT introduce interpretations that are not directly supported
by the analytical report.

RULES:

- Use ONLY the analytical report above.
- Do not invent facts, numbers, categories, or explanations.
- Do not calculate new metrics.
- Do not contradict the analytical report.
- Preserve the distinction between:
  * growth drivers
  * growth drags
  * decline drivers
  * decline offsets
- Use the exact numbers provided in the report.
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