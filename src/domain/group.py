from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    group_id: UUID
    name: str
    budget: float