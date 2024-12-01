from pydantic import BaseModel
from uuid import UUID

class Group(BaseModel):
    group_id: UUID
    name: str
    total_budget: float