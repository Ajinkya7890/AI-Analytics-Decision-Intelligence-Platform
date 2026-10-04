from src.ai.llm_client import OpenAILLMClient


client = OpenAILLMClient()

prompt = """
You are a business analytics assistant.

Explain this evidence in one concise paragraph:

Revenue increased from ₹6,155,806.98
to ₹7,386,050.80, an increase of 19.99%.

The largest growth contributor was health_beauty,
with a revenue contribution of ₹290,482.44.

Its primary growth driver was ORDER_VOLUME,
with an effect of ₹286,153.51.

Its growth drag was AVERAGE_PRICE,
with an effect of -₹9,367.15.

Do not invent any additional facts or numbers.
"""

response = client.generate(prompt)

print("OPENAI LLM TEST")
print("=" * 80)
print(response)