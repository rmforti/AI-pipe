from app.services.document_service import document_service
from app.services.llm_service import llm_service


class RAGService:
    def __init__(self):
        self._document_service = document_service
        self._llm_service = llm_service

    def ask(self, question: str, top_k: int = 3):
        search_response = self._document_service.search(question, top_k)

        chunks = search_response["results"]

        context = "\n\n".join(
            chunk["text"] for chunk in chunks
        )

        prompt = f"""
           Answer the user's question using only the context below.

        Context:
            {context}

        Question:
            {question}
            """

        answer = self._llm_service.generate_answer(prompt)

        return {
            "question": question,
            "answer": answer,
            "debug": {
                "query_embedding": search_response["query_embedding"],
                "retrieved_chunk_count": len(chunks),
                "context_length": len(context),
                "context": context,
            },
            "sources": chunks,
        }

rag_service = RAGService()