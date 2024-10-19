from fastapi import APIRouter
from src.domain.Repository.user_repository import UserRepository

from uuid import UUID

router = APIRouter()
user_repo = UserRepository()

@router.get("/")
async def get_all_users():
    users = await user_repo.get_users()
    return users

@router.get("/user/{user_id}")
async def get_user_by_id(user_id: UUID):
    user = await user_repo.get_user_by_id(user_id)
    return user

@router.get("/{group_id}")
async def get_users_by_group(group_id: UUID):
    users = await user_repo.get_users_by_group(group_id)
    return users