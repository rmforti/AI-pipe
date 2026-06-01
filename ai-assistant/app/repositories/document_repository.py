from uuid import UUID

from app.db.database import get_connection
from app.models.document import Document


class DocumentRepository:
    def create_document(self, document: Document) -> Document:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO documents (id, title, content) VALUES (?, ?, ?)",
                (str(document.id), document.title, document.content),
            )

        return document

    def list_documents(self) -> list[Document]:
        with get_connection() as conn:
            rows = conn.execute("SELECT id, title, content FROM documents").fetchall()

        return [
            Document(id=UUID(row["id"]), title=row["title"], content=row["content"])
            for row in rows
        ]

    def get_document(self, document_id: UUID) -> Document | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, title, content FROM documents WHERE id = ?",
                (str(document_id),),
            ).fetchone()

        if row is None:
            return None

        return Document(id=UUID(row["id"]), title=row["title"], content=row["content"])


document_repository = DocumentRepository()