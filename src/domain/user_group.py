from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserGroup(BaseModel):
    user_id: UUID
    group_id: UUID
    user_group_budget: Optional[float] = None

