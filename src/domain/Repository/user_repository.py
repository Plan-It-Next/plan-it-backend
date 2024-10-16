import asyncpg
from ..database import Database
from src.infraestructure.user import User

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
        sql = "SELECT * FROM users WHERE id = $1;"
        try:
            user = await conn.fetch(sql, id1)
            user = user[0]
            if user:
                return User(**dict(user))
            return None
        except Exception as e:
            raise Exception(f"Error : {str(e)}")