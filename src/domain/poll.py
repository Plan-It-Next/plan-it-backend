from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Poll(BaseModel):
    poll_id: UUID
    group_id: UUID
    poll_name: str
    poll_date: datetime

