from src.ai.question_analyzer import analyze_question
from src.ai.root_cause_engine import analyze_root_cause
from src.ai.investigation_result import build_investigation_result


def investigate(question):
    """
    Run an analytical investigation from a natural-language question.

    Current supported investigation:
        Revenue root-cause analysis between two years.
    """

    analysis = analyze_question(question)

    if analysis["intent"] != "root_cause":
        return {
            "status": "unsupported",
            "question": question,
            "message": (
                "The investigation engine currently supports "
                "revenue root-cause questions."
            ),
            "analysis": analysis
        }

    time_period = analysis.get("time_period", [])

    if len(time_period) < 2:
        return {
            "status": "insufficient_information",
            "question": question,
            "message": (
                "Two years are required for revenue "
                "root-cause analysis."
            ),
            "analysis": analysis
        }

    previous_year = int(time_period[0])
    current_year = int(time_period[1])

    root_cause_result = analyze_root_cause(
        current_year=current_year,
        previous_year=previous_year
    )

    investigation_result = build_investigation_result(
        root_cause_result
    )

    return {
        "status": "success",
        "question": question,
        "analysis": analysis,
        "investigation": investigation_result
    }