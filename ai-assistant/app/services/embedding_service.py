from uuid import UUID, uuid4

from openai import OpenAI

from app.core.config import OPENAI_EMBEDDING_MODEL
from app.models.embedding import Embedding


class EmbeddingService:
    def __init__(self):
        self._client = OpenAI()

    def generate_embedding(
        self,
        chunk_id: UUID,
        text: str,
    ) -> Embedding:
        vector = self._embed(text)

        return Embedding(
            id=uuid4(),
            chunk_id=chunk_id,
            model=OPENAI_EMBEDDING_MODEL,
            vector=vector,
        )

    def embed_text(self, text: str) -> Embedding:
        vector = self._embed(text)

        return Embedding(
            id=uuid4(),
            chunk_id=uuid4(),  # dummy ID for query embeddings
            model=OPENAI_EMBEDDING_MODEL,
            vector=vector,
        )

    def _embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding


embedding_service = EmbeddingService()