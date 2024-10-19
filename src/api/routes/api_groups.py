from fastapi import APIRouter
from src.domain.Repository.group_repository import GroupRepository
from uuid import UUID

router = APIRouter()
group_repo = GroupRepository()


@router.get("/")
async def get_all_groups():
    groups = await group_repo.get_groups()
    return groups


@router.get("/{user_id}")
async def get_groups_by_user(user_id: UUID):
    groups = await group_repo.get_groups_by_user(user_id)
    return groups