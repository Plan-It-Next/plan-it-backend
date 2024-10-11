from ..database import Database
from src.domain.user import User
from src.domain.group import Group

class GroupRepository:

    def __init__(self):
        self.conn = Database()

    async def get_groups(self):
        conn = await self.conn.get_conn()
        sql = "SELECT * FROM groups;"
        try:
            groups = await conn.fetch(sql)
            return [Group(**dict(group)) for group in groups]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_groups_by_user(self,id1):
        conn = await self.conn.get_conn()
        sql = '''SELECT g.group_id, g.name, g.budget
                    FROM user_group ug
                    JOIN groups g ON ug.group_id = g.group_id
                    WHERE ug.user_id = $1;'''
        try:
            rows = await conn.fetch(sql,id1)
            return [Group(**dict(row)) for row in rows]
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

