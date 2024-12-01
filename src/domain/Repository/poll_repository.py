from ..database import Database
from src.domain.poll import Poll, PollReq

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
            print(poll)
            return Poll(**dict(poll))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

