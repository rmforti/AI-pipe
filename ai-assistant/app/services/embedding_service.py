from uuid import UUID, uuid4

from openai import OpenAI

from app.core.config import OPENAI_EMBEDDING_MODEL
from app.models.embedding import Embedding

class EmbeddingServiceError(Exception):
    pass

class EmbeddingService:
    def __init__(self):
        self._openai_client = OpenAI()

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

    def embed_text(self, text: str) -> list[float]:
        try:
            response = self._openai_client.embeddings.create(
                model=OPENAI_EMBEDDING_MODEL,
                input=text,
            )

            return response.data[0].embedding

        except Exception as error:
            raise EmbeddingServiceError("Failed to generate embedding from OpenAI") from error

    def _embed(self, text: str) -> list[float]:
        response = self._openai_client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=text,
        )

        return response.data[0].embedding


embedding_service = EmbeddingService()