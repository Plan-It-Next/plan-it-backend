from ..database import Database
from src.domain.poll import Poll, PollReq, PollMod

class PollRepository:

    def __init__(self):
        self.conn = Database()

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
            print(poll)
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
