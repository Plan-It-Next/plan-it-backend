from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.poll_repository import PollRepository
from uuid import UUID
from src.domain.poll import Poll, PollReq, PollMod

router = APIRouter()
poll_repo = PollRepository()


@router.post("/create", response_model=Poll)
async def create_poll(poll: PollReq):
    try:
        poll = await poll_repo.create_poll(poll)
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


@router.put("/modify", response_model=Poll)
async def change_poll_name(poll: PollMod):
    try:
        poll = await poll_repo.change_poll_name(poll)
        if not poll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error modifying poll"
            )
        return poll
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while modifying poll"
        )


@router.delete("/delete")
async def delete_poll(poll: PollMod):
    try:
        poll_bool = await poll_repo.delete_poll(poll)
        if not poll_bool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error deleting poll"
            )
        return poll_bool
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting poll"
        )