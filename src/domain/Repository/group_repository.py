from ..database import Database
from src.domain.user import User
from src.domain.group import Group

class GroupRepository:

    def __init__(self):
        self.conn = Database()

    async def get_groups(self):
        conn = await self.conn.get_conn()
        sql = '''select g.group_id, g.name, sum( ug.user_group_budget) as total_budget
                    from groups g 
                    join user_group ug ON g.group_id = ug.group_id
                    group by g.group_id'''
        try:
            groups = await conn.fetch(sql)
            return [Group(**dict(group)) for group in groups]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def get_groups_by_user(self,id1):
        conn = await self.conn.get_conn()
        sql = '''SELECT g.group_id, g.name, (SELECT SUM(ug_inner.user_group_budget)
                                                FROM user_group ug_inner
                                                WHERE ug_inner.group_id = g.group_id) AS total_budget
                    FROM user_group ug
                    JOIN groups g ON ug.group_id = g.group_id
                    WHERE ug.user_id = $1
                    GROUP BY g.group_id, g.name;'''
        try:
            rows = await conn.fetch(sql,id1)
            return [Group(**dict(row)) for row in rows]
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

