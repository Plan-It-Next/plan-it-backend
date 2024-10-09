import asyncpg
from ..database import Database


class User_repository:

    def __init__(self):
        self.conn = Database()

    async def get_user(self):
        conn = await self.conn.get_conn()
        sql = "SELECT * FROM users;"
        try:
            return await conn.fetch(sql)
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_user_by_id(self, id1):
        conn = await self.conn.get_conn()
        sql = "SELECT * FROM User WHERE userid = $1;"
        try:
            return await conn.fetch(sql, id1)
        except Exception as e:
            raise Exception(f"Error : {str(e)}")