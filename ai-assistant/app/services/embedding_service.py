from uuid import UUID, uuid4
from app.models.embedding import Embedding


class EmbeddingService:
    def generate_embedding(
        self,
        chunk_id: UUID,
        text: str,
    ) -> Embedding:
        return Embedding(
            id=uuid4(),
            chunk_id=chunk_id,
            model="fake-character-count-v1",
            vector=[
                float(len(text)),
                float(text.lower().count("a")),
                float(text.lower().count("e")),
            ],
        )

    def embed_text(self, text: str) -> Embedding:
        return Embedding(
            id=uuid4(),
            chunk_id=uuid4(),  # temporary/dummy for query embeddings
            model="fake-character-count-v1",
            vector=[
                len(text),
                text.lower().count("a"),
                text.lower().count("e"),
            ],
        )


embedding_service = EmbeddingService()