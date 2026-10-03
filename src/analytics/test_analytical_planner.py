from src.analytics.analytical_planner import create_plan


questions = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "What is the average delivery time?",
    "Why did revenue decrease in 2018?"
]


for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    plan = create_plan(question)

    print("\nANALYTICAL PLAN:")
    print(plan)