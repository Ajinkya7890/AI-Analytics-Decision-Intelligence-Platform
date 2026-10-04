from src.ai.investigator import investigate
from src.ai.explanation_engine import ExplanationEngine
from src.ai.llm_client import OllamaLLMClient


QUESTION = "Why did revenue decrease between 2017 and 2018?"


print("FULL AI INVESTIGATION TEST")
print("=" * 80)


# --------------------------------------------------
# Step 1 — Run the complete investigation
# --------------------------------------------------

result = investigate(QUESTION)


print("\nINVESTIGATION STATUS")
print("-" * 80)
print(result["status"])


if result["status"] != "success":

    print("\nInvestigation failed:")
    print(result)

    raise SystemExit(1)


# --------------------------------------------------
# Step 2 — Get structured investigation report
# --------------------------------------------------

investigation = result["investigation"]


print("\nSTRUCTURED INVESTIGATION")
print("-" * 80)

period = investigation["period"]
overall = investigation["overall"]


print(
    f"Period: "
    f"{period['previous_year']} → "
    f"{period['current_year']}"
)

print(
    f"Revenue change: "
    f"₹{overall['revenue_change']:,.2f}"
)

print(
    f"Percentage change: "
    f"{overall['percentage_change']:+.2f}%"
)


# --------------------------------------------------
# Step 3 — Connect Ollama / Gemma
# --------------------------------------------------

llm_client = OllamaLLMClient()

explanation_engine = ExplanationEngine(
    llm_client=llm_client
)


# --------------------------------------------------
# Step 4 — Generate business explanation
# --------------------------------------------------

explanation_result = explanation_engine.explain(
    question=QUESTION,
    investigation_report=investigation
)


# --------------------------------------------------
# Step 5 — Display AI explanation
# --------------------------------------------------

print("\nGEMMA BUSINESS EXPLANATION")
print("-" * 80)

print(
    explanation_result["explanation"]
)