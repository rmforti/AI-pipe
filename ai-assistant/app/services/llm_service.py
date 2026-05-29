class LLMService:
    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:
        prompt = self._build_prompt(question, context)

        return (
            "This is a fake LLM answer.\n\n"
            f"Prompt sent to LLM:\n\n{prompt}"
        )

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