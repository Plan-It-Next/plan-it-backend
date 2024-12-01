from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.user_group_repository import UserGroupRepository
from typing import List
from uuid import UUID
from src.domain.user_group import UserGroup

router = APIRouter()
user_group_repo = UserGroupRepository()


@router.get("/{user_id}/{group_id}", response_model=UserGroup)
async def get_user_group(user_id: UUID, group_id: UUID):
    try:
        ug = await user_group_repo.get_user_group(user_id, group_id)
        if not ug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user_group found"
            )
        return ug

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching user_group"
        )


@router.put("/budget", response_model=UserGroup)
async def set_user_group_budget(user_group: UserGroup):
    try:
        ug = await user_group_repo.set_user_group_budget(user_group)
        if not ug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No groups found"
            )
        return ug
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user group: {str(e)}"
        )