from src.ai.question_analyzer import analyze_question


questions = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "Why did revenue decrease in 2018?",
    "What is the average delivery time?",
    "Compare revenue between sellers."
]


for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:")
    print(question)

    result = analyze_question(question)

    print("\nANALYSIS:")
    print(result)