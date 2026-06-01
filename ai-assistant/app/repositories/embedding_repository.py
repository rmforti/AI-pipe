import json
from uuid import UUID

from app.db.database import get_connection
from app.models.embedding import Embedding


class EmbeddingRepository:
    def create_embedding(self, embedding: Embedding) -> Embedding:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO embeddings (id, chunk_id, model, vector) VALUES (?, ?, ?, ?)",
                (str(embedding.id), str(embedding.chunk_id), embedding.model, json.dumps(embedding.vector)),
            )

        return embedding

    def list_embeddings(self) -> list[Embedding]:
        with get_connection() as conn:
            rows = conn.execute("SELECT id, chunk_id, model, vector FROM embeddings").fetchall()

        return [
            Embedding(id=UUID(row["id"]), chunk_id=UUID(row["chunk_id"]), model=row["model"], vector=json.loads(row["vector"]))
            for row in rows
        ]

    def get_embedding_by_chunk_id(self, chunk_id: UUID) -> Embedding | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, chunk_id, model, vector FROM embeddings WHERE chunk_id = ?",
                (str(chunk_id),),
            ).fetchone()

        if row is None:
            return None

        return Embedding(id=UUID(row["id"]), chunk_id=UUID(row["chunk_id"]), model=row["model"], vector=json.loads(row["vector"]))


embedding_repository = EmbeddingRepository()