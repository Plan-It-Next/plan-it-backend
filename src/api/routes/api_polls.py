from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.poll_repository import PollRepository
from uuid import UUID
from src.domain.poll import Poll, PollReq

router = APIRouter()
poll_repo = PollRepository()


@router.post("/create", response_model=Poll)
async def get_user_group(poll: PollReq):
    try:
        poll = await poll_repo.create_poll(poll)
        print(poll)
        if not poll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error creating poll"
            )
        return poll

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating poll"
        )