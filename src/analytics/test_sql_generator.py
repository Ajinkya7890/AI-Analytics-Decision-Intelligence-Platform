from src.analytics.sql_generator import generate_sql


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

    sql = generate_sql(question)

    print("\nGENERATED SQL:")
    print(sql)