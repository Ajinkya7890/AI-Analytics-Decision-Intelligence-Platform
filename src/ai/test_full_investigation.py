from src.ai.investigator import investigate
from src.ai.investigation_report import build_investigation_report
from src.ai.root_cause_engine import analyze_root_cause
from src.ai.explanation_engine import ExplanationEngine
from src.ai.llm_client import OllamaLLMClient


QUESTION = "Why did revenue decrease between 2017 and 2018?"

PREVIOUS_YEAR = 2017
CURRENT_YEAR = 2018


print("FULL AI INVESTIGATION TEST")
print("=" * 80)


# Step 1: Analyze the user's question
result = investigate(QUESTION)


print("\nINVESTIGATION STATUS")
print("-" * 80)
print(result["status"])


if result["status"] != "success":
    print("\nInvestigation failed:")
    print(result)
    raise SystemExit(1)


# Step 2: Run the root-cause engine
root_cause_result = analyze_root_cause(
    current_year=CURRENT_YEAR,
    previous_year=PREVIOUS_YEAR
)


# Step 3: Build the structured investigation report
report = build_investigation_report(
    root_cause_result
)


print("\nSTRUCTURED REPORT")
print("-" * 80)

print(
    f"Period: "
    f"{report['period'][0]} → {report['period'][1]}"
)

print(
    f"Revenue change: "
    f"₹{report['overall_result']['revenue_change']:,.2f}"
)

print(
    f"Revenue growth: "
    f"{report['overall_result']['percentage_change']:.2f}%"
)


# Step 4: Connect Ollama / Gemma
llm_client = OllamaLLMClient()

explanation_engine = ExplanationEngine(
    llm_client=llm_client
)


# Step 5: Generate the business explanation
explanation_result = explanation_engine.explain(
    question=QUESTION,
    investigation_report=report
)


print("\nGEMMA BUSINESS EXPLANATION")
print("-" * 80)
print(explanation_result["explanation"])