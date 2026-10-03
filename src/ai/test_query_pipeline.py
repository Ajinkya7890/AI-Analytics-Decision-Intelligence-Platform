from src.ai.query_pipeline import run_question


questions = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "What is the average delivery time?"
]


for question in questions:

    print("\n" + "=" * 80)

    print("QUESTION:")
    print(question)

    try:

        result = run_question(question)

        print("\nSQL:")
        print(result["sql"])

        print("\nVALIDATION:")
        print(result["validation"])

        print("\nCOLUMNS:")
        print(result["columns"])

        print("\nRESULTS:")

        for row in result["rows"][:10]:
            print(row)

    except Exception as error:

        print("\nERROR:")
        print(error)