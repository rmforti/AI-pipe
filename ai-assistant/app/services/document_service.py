from uuid import UUID, uuid4
import math

from app.core.config import MAX_UPLOAD_FILE_SIZE_BYTES, SUPPORTED_UPLOAD_EXTENSIONS

from app.models.document import Document
from app.models.chunk import Chunk
from app.models.embedding import Embedding

from app.services.embedding_service import embedding_service
from app.services.file_parsing_service import file_parsing_service
from app.services.chunking_service import chunking_service

from app.repositories.document_repository import document_repository
from app.repositories.chunk_repository import chunk_repository
from app.repositories.embedding_repository import embedding_repository


class DocumentService:
    def __init__(self) -> None:
        self._embedding_service = embedding_service
        self._file_parsing_service = file_parsing_service
        self._chunking_service = chunking_service
        self._document_repository = document_repository
        self._chunk_repository = chunk_repository
        self._embedding_repository = embedding_repository

    def create_document(self, title: str, content: str) -> Document:
        if title.strip() == "":
            raise ValueError("Document title cannot be empty")

        if content.strip() == "":
            raise ValueError("Document content cannot be empty")

        document = Document(id=uuid4(), title=title, content=content)

        self._document_repository.create_document(document)

        chunks = self._chunking_service.chunk_text(document.id, document.content)
        self._chunk_repository.create_chunks(chunks)

        for chunk in chunks:
            embedding = self._embedding_service.generate_embedding(chunk_id=chunk.id, text=chunk.text)
            self._embedding_repository.create_embedding(embedding)

        return document

    def create_document_from_upload(self, filename: str, raw_content: bytes) -> Document:
        if filename.strip() == "":
            raise ValueError("Uploaded file must have a filename")

        normalized_filename = filename.lower()

        if not normalized_filename.endswith(SUPPORTED_UPLOAD_EXTENSIONS):
            raise ValueError("Only .txt, .md, and .pdf files are supported")

        if len(raw_content) > MAX_UPLOAD_FILE_SIZE_BYTES:
            raise ValueError("File is too large. Maximum size is 1 MB")

        content = self._file_parsing_service.parse_file(filename=filename, raw_content=raw_content)

        return self.create_document(title=filename, content=content)

    def list_documents(self) -> list[Document]:
        return self._document_repository.list_documents()

    def get_document(self, document_id: UUID) -> Document | None:
        return self._document_repository.get_document(document_id)

    def get_chunks(self, document_id: UUID) -> list[Chunk] | None:
        if self.get_document(document_id) is None:
            return None

        return self._chunk_repository.get_chunks_by_document_id(document_id)

    def get_embedding_for_chunk(self, chunk_id: UUID) -> Embedding | None:
        return self._embedding_repository.get_embedding_by_chunk_id(chunk_id)

    def list_embeddings(self) -> list[Embedding]:
        return self._embedding_repository.list_embeddings()

    def search(self, query: str, top_k: int = 3):
        query_embedding = self._embedding_service.embed_text(query)

        chunks_with_embeddings = self._chunk_repository.list_chunks_with_embeddings()

        results = []

        for chunk, chunk_embedding_vector in chunks_with_embeddings:
            score = self._similarity_score(query_embedding, chunk_embedding_vector)

            results.append({
                "score": score,
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        return {"query": query, "query_embedding": query_embedding, "results": results[:top_k]}

    def _similarity_score(self, a: list[float], b: list[float]) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))

        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(y * y for y in b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)


document_service = DocumentService()