from pydantic import BaseModel
from uuid import UUID, uuid4


class Chunk(BaseModel):
    id: UUID
    document_id: UUID
    text: str
    chunk_index: int