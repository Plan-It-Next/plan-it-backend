from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Poll(BaseModel):
    poll_id: UUID
    group_id: UUID
    poll_name: str
    poll_date: datetime

class PollReq(BaseModel):
    group_id: UUID
    poll_name: str

class PollMod(BaseModel):
    poll_id: UUID
    poll_name: str

class PollAndVotes(BaseModel):
    poll_id: UUID
    poll_name: str
    poll_date: datetime
    total_votes: int
    true_votes: int

