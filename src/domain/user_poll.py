from pydantic import BaseModel
from uuid import UUID

class UserPoll(BaseModel):
    poll_id: UUID
    user_id: UUID
    group_id: UUID
    vote: bool

