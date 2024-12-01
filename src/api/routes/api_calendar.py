from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.calendar_repository import CalendarRepository
from uuid import UUID
from typing import List
from src.domain.user_calendar import UserCalendar, UserAvDay, AvDay
from src.domain.user_group import UserGroup

router = APIRouter()
calendar_repo = CalendarRepository()


@router.post("/add_day")
async def add_av_day(av_days: List[UserCalendar]):
    try:
        for day in av_days:
            free_day = await calendar_repo.add_day(day)
            if not free_day:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Error adding day"
                )
        return True
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding days"
        )


@router.get("/{group_id}", response_model=List[AvDay])
async def get_common_days_by_group_id(group_id: UUID):
    try:
        days = await calendar_repo.get_common_days(group_id)
        if not days:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error getting common days"
            )
        return days
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting days"
        )


@router.get("/{user_id}/{group_id}", response_model=List[UserCalendar])
async def get_user_days(user_id: UUID, group_id: UUID):
    try:
        days = await calendar_repo.get_user_days(user_id, group_id)
        if not days:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error getting user_group days"
            )
        return days
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting user_group_days"
        )