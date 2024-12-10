from ..database import Database
from src.domain.poll import Poll, PollReq, PollMod, PollAndVotes
from src.domain.user_poll import UserPoll, PollAndUserGroup
import logging

class PollRepository:

    def __init__(self):
        self.conn = Database()


    async def get_poll_vote(self, poll_vote: UserPoll):
        conn = await self.conn.get_conn()
        sql = '''SELECT poll_id, user_id, group_id, vote
                    FROM user_polls
                    WHERE poll_id = $1 and user_id = $2 and group_id = $3'''
        try:
            poll = await conn.fetchrow(sql, poll_vote.poll_id, poll_vote.user_id, poll_vote.group_id)
            if not poll:
                return None
            return UserPoll(**dict(poll))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def create_poll(self, poll: PollReq):
        conn = await self.conn.get_conn()
        sql = '''INSERT INTO polls (group_id, poll_name)
                    VALUES ($1, $2)
                    RETURNING poll_id, group_id, poll_name, poll_date;'''
        try:
            poll = await conn.fetchrow(sql, poll.group_id, poll.poll_name)
            return Poll(**dict(poll))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def change_poll_name(self, poll: PollMod):
        conn = await self.conn.get_conn()
        sql = '''UPDATE polls
                    SET poll_name = $1
                    WHERE poll_id = $2
                    RETURNING poll_id, group_id, poll_name, poll_date;'''
        try:
            poll = await conn.fetchrow(sql, poll.poll_name, poll.poll_id)
            return Poll(**dict(poll))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def delete_poll(self, poll: PollMod):
        conn = await self.conn.get_conn()
        sql = '''DELETE FROM polls
                    WHERE poll_id = $1
                    RETURNING poll_id;'''
        try:
            result = await conn.fetchrow(sql, poll.poll_id)
            if result is None:
                return False
            return True
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def get_group_polls(self, group_id):
        conn = await self.conn.get_conn()
        sql = '''SELECT p.poll_id, p.poll_name, p.poll_date,
                        COUNT(up.user_id) AS total_votes, 
                        COUNT(CASE WHEN up.vote THEN 1 END) AS true_votes 
                    FROM polls p
                    LEFT JOIN user_polls up
                    ON p.poll_id = up.poll_id
                    WHERE p.group_id = $1
                    GROUP BY p.poll_id, p.poll_name, p.poll_date
                    ORDER BY p.poll_date DESC;'''
        try:
            polls = await conn.fetch(sql, group_id)
            print(polls)
            return [PollAndVotes(**dict(poll)) for poll in polls]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def get_poll_votes(self, group_id, poll_id):
        conn = await self.conn.get_conn()
        sql = '''SELECT up.poll_id, up.user_id, up.group_id, up.vote, (SELECT COUNT(*) FROM user_group ug WHERE ug.group_id = $1) AS total_users_group
                    FROM user_polls up
                    WHERE poll_id = $2;'''
        try:
            polls = await conn.fetch(sql, group_id, poll_id)
            return [PollAndUserGroup(**dict(poll)) for poll in polls]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def vote_poll(self, poll_vote: UserPoll):
        conn = await self.conn.get_conn()
        sql = '''INSERT INTO user_polls (poll_id, user_id, group_id, vote)
                    VALUES ($1, $2, $3, $4)
                    RETURNING poll_id, user_id, group_id, vote'''
        try:
            p_vote = await conn.fetchrow(sql, poll_vote.poll_id, poll_vote.user_id, poll_vote.group_id, poll_vote.vote)
            print(p_vote)
            return UserPoll(**dict(p_vote))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def update_vote_poll(self, poll_vote: UserPoll):
        conn = await self.conn.get_conn()
        sql = '''UPDATE user_polls
                    SET vote = $1
                    WHERE poll_id = $2 AND user_id = $3 AND group_id = $4
                    RETURNING poll_id, user_id, group_id, vote'''
        try:
            p_vote = await conn.fetchrow(sql, poll_vote.vote, poll_vote.poll_id, poll_vote.user_id, poll_vote.group_id,)
            return UserPoll(**dict(p_vote))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")