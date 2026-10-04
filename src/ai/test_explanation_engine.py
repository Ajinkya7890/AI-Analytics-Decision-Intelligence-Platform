from src.ai.question_analyzer import analyze_question
from src.ai.root_cause_engine import analyze_root_cause
from src.ai.investigation_report import build_investigation_report
from src.ai.explanation_engine import ExplanationEngine
from src.ai.llm_client import MockLLMClient


question = "Why did revenue decrease between 2017 and 2018?"

analysis = analyze_question(question)


if analysis["intent"] != "root_cause":

    print("Unsupported investigation question.")

else:

    time_period = analysis.get("time_period", [])

    if len(time_period) < 2:

        print("Two years are required for investigation.")

    else:

        previous_year = int(time_period[0])
        current_year = int(time_period[1])

        root_cause_result = analyze_root_cause(
            current_year=current_year,
            previous_year=previous_year
        )

        investigation_report = build_investigation_report(
            root_cause_result
        )

        client = MockLLMClient()

        engine = ExplanationEngine(
            llm_client=client
        )

        result = engine.explain(
            question=question,
            investigation_report=investigation_report
        )

        print("EXPLANATION ENGINE TEST")
        print("=" * 100)

        print("\nSTRUCTURED INVESTIGATION REPORT")
        print("-" * 100)

        print(investigation_report)

        print("\nPROMPT SENT TO LLM")
        print("-" * 100)

        print(result["prompt"])

        print("\nLLM RESPONSE")
        print("-" * 100)

        print(result["explanation"])