from src.ai.question_analyzer import analyze_question
from src.ai.investigation_strategies import (
    create_default_registry
)


def investigate(question):
    """
    Run an analytical investigation from a natural-language question.

    The investigator acts as an orchestration layer:

        Question
            ↓
        Question Analyzer
            ↓
        Strategy Registry
            ↓
        Matching Investigation Strategy
            ↓
        Structured Investigation Result
    """

    analysis = analyze_question(question)

    registry = create_default_registry()

    strategy = registry.get_strategy(analysis)

    if strategy is None:

        return {
            "status": "unsupported",
            "question": question,
            "message": (
                "No investigation strategy currently supports "
                "this analytical question."
            ),
            "analysis": analysis
        }

    try:

        investigation_result = strategy.investigate(
            analysis
        )

    except ValueError as error:

        return {
            "status": "error",
            "question": question,
            "message": str(error),
            "analysis": analysis,
            "strategy": strategy.name
        }

    return {
        "status": "success",
        "question": question,
        "analysis": analysis,
        "strategy": strategy.name,
        "strategy_description": strategy.description,
        "investigation": investigation_result
    }