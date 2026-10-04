from src.analytics.sql_generator import generate_sql


TEST_QUESTIONS = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "Which sellers generated the highest revenue?",
    "What is the average delivery time?",
    "What caused the decline in sales in 2018?",
]


def main():
    for question in TEST_QUESTIONS:

        print("=" * 70)
        print("QUESTION:")
        print(question)

        try:
            sql = generate_sql(question)

            print("\nGENERATED SQL:")
            print(sql)

        except Exception as error:

            print("\nERROR:")
            print(error)

        print()


if __name__ == "__main__":
    main()