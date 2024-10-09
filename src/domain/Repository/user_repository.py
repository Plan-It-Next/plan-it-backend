import asyncpg
from ..database import Database


class User_repository:

    def __init__(self):
        self.conn = Database()

    async def get_user(self):
        conn = self.conn.get_conn()
        sql = "SELECT * FROM User;"
        try:
            return await conn.fetchval(sql)
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_user_by_id(self, id1):
        conn = self.conn.get_conn()
        sql = "SELECT * FROM User WHERE userid = $1;"
        try:
            return await conn.execute(sql, id1)
        except Exception as e:
            raise Exception(f"Error : {str(e)}")