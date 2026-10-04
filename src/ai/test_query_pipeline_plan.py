from src.ai.query_pipeline import run_question


question = "Which products generated the highest revenue?"

result = run_question(question)

print("=" * 80)
print("QUESTION:")
print(result["question"])

print("\nANALYTICAL PLAN:")
print(result["plan"])

print("\nSQL:")
print(result["sql"])

print("\nVALIDATION:")
print(result["validation"])

print("\nCOLUMNS:")
print(result["columns"])

print("\nFIRST 5 RESULTS:")
for row in result["rows"][:5]:
    print(row)