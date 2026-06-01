import json
from uuid import UUID

from app.db.database import get_connection
from app.models.chunk import Chunk

class ChunkRepository:
    def create_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        with get_connection() as conn:
            conn.executemany(
                "INSERT INTO chunks (id, document_id, chunk_index, text) VALUES (?, ?, ?, ?)",
                [(str(chunk.id), str(chunk.document_id), chunk.chunk_index, chunk.text) for chunk in chunks],
            )

        return chunks

    def get_chunks_by_document_id(self, document_id: UUID) -> list[Chunk]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, document_id, chunk_index, text FROM chunks WHERE document_id = ? ORDER BY chunk_index",
                (str(document_id),),
            ).fetchall()

        return [
            Chunk(id=UUID(row["id"]), document_id=UUID(row["document_id"]), chunk_index=row["chunk_index"], text=row["text"])
            for row in rows
        ]

    def list_chunks_with_embeddings(self) -> list[tuple[Chunk, list[float]]]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    chunks.id,
                    chunks.document_id,
                    chunks.chunk_index,
                    chunks.text,
                    embeddings.vector
                FROM chunks
                JOIN embeddings
                    ON embeddings.chunk_id = chunks.id
                """
            ).fetchall()

        return [
            (
                Chunk(id=UUID(row["id"]), document_id=UUID(row["document_id"]), chunk_index=row["chunk_index"], text=row["text"]),
                json.loads(row["vector"]),
            )
            for row in rows
        ]

chunk_repository = ChunkRepository()