from src.ai.llm_client import MockLLMClient


client = MockLLMClient()

prompt = """
Explain the following analytical evidence:

Revenue increased by 19.99%.
The primary growth driver was order volume.
"""

response = client.generate(prompt)

print("LLM CLIENT TEST")
print("=" * 80)
print(response)