from src.ai.question_analyzer import analyze_question


questions = [
    "What were the total sales by category in 2018?",
    "How many orders did we receive?",
    "How many units were sold?",
    "What was the turnover by seller?",
    "Show the yearly revenue trend.",
    "What was the average rating by product category?",
    "Compare sales between vendors.",
    "What caused the decline in sales in 2018?"
]


for question in questions:
    print("=" * 80)
    print(f"QUESTION: {question}")
    print("ANALYSIS:")
    print(analyze_question(question))