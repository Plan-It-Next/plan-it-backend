from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.group_repository import GroupRepository
from typing import List
from uuid import UUID
from src.domain.group import Group

router = APIRouter()
group_repo = GroupRepository()


@router.get("/", response_model=List[Group])
async def get_all_groups():
    try:
        groups = await group_repo.get_groups()
        if not groups:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No groups found"
            )
        return groups

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching groups"
        )


@router.get("/{user_id}", response_model=List[Group])
async def get_groups_by_user(user_id: UUID):
    try:
        groups = await group_repo.get_groups_by_user(user_id)
        if not groups:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No groups found"
            )
        return groups

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching groups"
        )