from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr