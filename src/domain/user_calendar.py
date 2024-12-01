from pydantic import BaseModel
from uuid import UUID
from datetime import date

class UserCalendar(BaseModel):
    user_id: UUID
    group_id: UUID
    available_day: date

class AvDay(BaseModel):
    available_day: date
    num_users: int

class UserAvDay(BaseModel):
    user_id: UUID
    available_day: date

