import ollama


class LLMClient:
    def generate(self, prompt):
        raise NotImplementedError(
            "LLM provider has not been configured yet."
        )


class OllamaLLMClient(LLMClient):
    def __init__(self, model="gemma3:4b"):
        self.model = model

    def generate(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]


class MockLLMClient(LLMClient):
    def generate(self, prompt):
        return (
            "MOCK LLM RESPONSE\n\n"
            "The LLM provider is not connected yet.\n"
            "The analytical evidence was successfully prepared."
        )