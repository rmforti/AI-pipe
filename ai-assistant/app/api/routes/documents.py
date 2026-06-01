from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import MAX_UPLOAD_FILE_SIZE_BYTES, SUPPORTED_UPLOAD_EXTENSIONS

from app.models.document import Document, DocumentCreate, DocumentSearchRequest, AskRequest
from app.services.document_service import document_service
from app.services.rag_service import rag_service
from app.services.llm_service import LLMServiceError
from app.services.embedding_service import EmbeddingServiceError

router = APIRouter(prefix="/documents", tags=["documents"])

class DocumentCreateRequest(BaseModel):
    title: str
    content: str


@router.post("")
def create_document(request: DocumentCreateRequest):
    try:
        return document_service.create_document(title=request.title, content=request.content)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except EmbeddingServiceError:
        raise HTTPException(status_code=502, detail="Failed to generate embedding from OpenAI")


@router.get("", response_model=list[Document])
def list_documents() -> list[Document]:
    return document_service.list_documents()


@router.get("/embeddings")
def list_embeddings():
    return document_service.list_embeddings()


@router.get("/chunks/{chunk_id}/embedding")
def get_chunk_embedding(chunk_id: UUID):
    embedding = document_service.get_embedding(chunk_id)

    if embedding is None:
        raise HTTPException(status_code=404, detail="Embedding not found")

    return embedding

@router.post("/search")
def search(request: DocumentSearchRequest):
    try:
        return document_service.search(request.query, request.top_k)

    except EmbeddingServiceError:
        raise HTTPException(status_code=502, detail="Failed to generate embedding from OpenAI")

@router.post("/ask")
def ask(request: AskRequest):
    try:
        return rag_service.ask(request.question, request.top_k)

    except LLMServiceError:
        raise HTTPException(status_code=502, detail="Failed to generate response from OpenAI")

MAX_FILE_SIZE_BYTES = 1_000_000
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename")

    try:
        raw_content = await file.read()
        return document_service.create_document_from_upload(filename=file.filename, raw_content=raw_content)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except EmbeddingServiceError:
        raise HTTPException(status_code=502, detail="Failed to generate embedding from OpenAI")

@router.get("/{document_id}/chunks")
def get_document_chunks(document_id: UUID):
    chunks = document_service.get_chunks(document_id)

    if chunks is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return chunks


@router.get("/{document_id}", response_model=Document)
def get_document(document_id: UUID) -> Document:
    document = document_service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return document
