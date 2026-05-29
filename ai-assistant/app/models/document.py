from uuid import UUID
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    content: str


class Document(BaseModel):
    id: UUID
    title: str
    content: str

class DocumentSearchRequest(BaseModel):
    query: str
    top_k: int = 3

class AskRequest(BaseModel):
    question: str
    top_k: int = 3