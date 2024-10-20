from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.user_repository import UserRepository
from typing import List
from uuid import UUID
from src.domain.user import User

router = APIRouter()
user_repo = UserRepository()

@router.get("/", response_model=List[User])
async def get_all_users():
    try:
        users = await user_repo.get_users()
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found"
            )
        return users
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching users"
        )


@router.get("/user/{user_id}", response_model=User)
async def get_user_by_id(user_id: UUID):
    try:
        user = await user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the user"
    )


@router.get("/{group_id}", response_model=List[User])
async def get_users_by_group(group_id: UUID):
    try:
        users = await user_repo.get_users_by_group(group_id)
        print(users)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found"
            )
        return users
    except HTTPException as he:
        raise he
    except Exception as e:
        print("An error occurred:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching users"
        )