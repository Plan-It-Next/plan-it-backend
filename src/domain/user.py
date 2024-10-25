from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr

class UserAll(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr
    password: str