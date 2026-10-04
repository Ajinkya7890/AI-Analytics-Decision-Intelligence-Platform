from src.ai.query_pipeline import run_question
from src.ai.query_explanation import QueryExplanationEngine
from src.ai.llm_client import OllamaLLMClient


question = "What is our total revenue?"

result = run_question(question)

client = OllamaLLMClient()

engine = QueryExplanationEngine(
    llm_client=client
)

explanation = engine.explain(
    question=question,
    plan=result["plan"],
    columns=result["columns"],
    rows=result["rows"],
    statistics=result["statistics"]
)

print("QUERY EXPLANATION TEST")
print("=" * 100)

print("\nQUESTION")
print("-" * 100)
print(question)

print("\nANALYTICAL PLAN")
print("-" * 100)
print(result["plan"])

print("\nGENERATED SQL")
print("-" * 100)
print(result["sql"])

print("\nSTATISTICS")
print("-" * 100)
print(result["statistics"])

print("\nLLM EXPLANATION")
print("-" * 100)
print(explanation["explanation"])