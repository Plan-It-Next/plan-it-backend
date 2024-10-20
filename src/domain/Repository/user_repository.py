from ..database import Database
from src.domain.user import User
from src.domain.group import Group

class UserRepository:

    def __init__(self):
        self.conn = Database()

    async def get_users(self):
        conn = await self.conn.get_conn()
        sql = "SELECT * FROM users;"
        try:
            users = await conn.fetch(sql)
            return [User(**dict(user)) for user in users]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_user_by_id(self, id1):
        conn = await self.conn.get_conn()
        sql = "SELECT * FROM users WHERE user_id = $1;"
        try:
            user = await conn.fetch(sql, id1)
            if user:
                return User(**dict(user[0]))
            return None
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_users_by_group(self, id1):
        conn = await self.conn.get_conn()
        sql = '''SELECT u.user_id, u.name, u.email
                    FROM user_group us
                    JOIN users u ON us.user_id = u.user_id
                    WHERE us.group_id = $1;'''
        try:
            users = await conn.fetch(sql, id1)
            return [User(**dict(user)) for user in users]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")