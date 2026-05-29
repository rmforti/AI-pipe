from uuid import UUID
from pydantic import BaseModel


class Embedding(BaseModel):
    id: UUID
    chunk_id: UUID
    model: str
    vector: list[float]