from fastapi import APIRouter, HTTPException, status
from src.domain.Repository.poll_repository import PollRepository
from src.domain.poll import Poll, PollReq, PollMod, PollAndVotes
from src.domain.user_poll import UserPoll, PollAndUserGroup
from uuid import UUID
from typing import List

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
    except Exception:
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
    except Exception:
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting poll"
        )


@router.post("/vote", response_model=UserPoll)
async def vote_poll(poll_vote: UserPoll):
    try:
        poll_voted = await poll_repo.get_poll_vote(poll_vote)
        if not poll_voted:
            print('not')
            return await poll_repo.vote_poll(poll_vote)
        else:
            print('yes')
            return await poll_repo.update_vote_poll(poll_vote)
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while voting poll"
        )


@router.get("/{group_id}", response_model=List[PollAndVotes])
async def get_polls_by_group_id(group_id: UUID):
    try:
        return await poll_repo.get_group_polls(group_id)
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting polls"
        )


@router.get("/{group_id}/{poll_id}", response_model=List[PollAndUserGroup])
async def get_poll_votes(group_id: UUID, poll_id: UUID):
    try:
        votes = await poll_repo.get_poll_votes(group_id, poll_id)
        return votes
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting polls"
        )