from openai import OpenAI
from app.core.config import OPENAI_MODEL

class LLMService:
    def __init__(self):
        self._client = OpenAI()

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:
        prompt = self._build_prompt(question, context)

        response = self._client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

        return response.output_text

    def _build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        return f"""
You are a helpful assistant.

Answer the user's question using only the context below.

If the answer is not in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}
"""


llm_service = LLMService()