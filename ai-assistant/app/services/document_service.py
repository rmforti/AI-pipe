from uuid import UUID, uuid4

import math

from app.models.document import Document, DocumentCreate

from app.models.chunk import Chunk
from app.services.chunking_service import chunking_service

from app.models.embedding import Embedding
from app.services.embedding_service import embedding_service

from pydantic import BaseModel

class DocumentService:
    def __init__(self) -> None:
        self._documents: dict[UUID, Document] = {}
        self._chunks: dict[UUID, list[Chunk]] = {}
        self._embeddings_by_chunk_id: dict[UUID, Embedding] = {}
        self._embedding_service = embedding_service

    def create_document(self, document_create: DocumentCreate) -> Document:
        document = Document(
            id=uuid4(),
            title=document_create.title,
            content=document_create.content,
        )

        self._documents[document.id] = document

        chunks = chunking_service.chunk_text(
            document_id=document.id,
            text=document.content,
        )

        self._chunks[document.id] = chunks

        for chunk in chunks:
            embedding = embedding_service.generate_embedding(
                chunk_id=chunk.id,
                text=chunk.text,
            )

            self._embeddings_by_chunk_id[chunk.id] = embedding

        return document

    def list_documents(self) -> list[Document]:
        return list(self._documents.values())

    def get_document(self, document_id: UUID) -> Document | None:
        return self._documents.get(document_id)

    def get_chunks(self, document_id: UUID) -> list[Chunk] | None:
        if document_id not in self._documents:
            return None

        return self._chunks.get(document_id, [])

    def get_embedding_for_chunk(self, chunk_id: UUID) -> Embedding | None:
        return self._embeddings_by_chunk_id.get(chunk_id)
            
    def list_embeddings(self) -> list[Embedding]:
        return list(self._embeddings_by_chunk_id.values())

    def search(self, query: str, top_k: int = 3):
        query_embedding = self._embedding_service.embed_text(query)

        results = []

        for document_chunks in self._chunks.values():
            for chunk in document_chunks:
                chunk_embedding = self._embeddings_by_chunk_id.get(chunk.id)

                if chunk_embedding is None:
                    continue

                score = self._similarity_score(
                    query_embedding.vector,
                    chunk_embedding.vector,
                )

                results.append({
                    "score": score,
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                    "embedding": chunk_embedding.vector,
                })

        results.sort(key=lambda item: item["score"], reverse=True)

        return {
            "query": query,
            "query_embedding": query_embedding.vector,
            "results": results[:top_k],
        }

    def _similarity_score(
        self,
        a: list[float],
        b: list[float],
    ) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))

        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(y * y for y in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

document_service = DocumentService()