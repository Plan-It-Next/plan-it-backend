from ..database import Database
from src.domain.user_group import UserGroup

class UserGroupRepository:

    def __init__(self):
        self.conn = Database()

    async def get_user_group(self, user_id, group_id):
        conn = await self.conn.get_conn()
        sql = '''SELECT * 
                    FROM user_group
                    WHERE user_id = $1 AND group_id = $2;'''
        try:
            ug = await conn.fetchrow(sql, user_id, group_id)
            return UserGroup(**dict(ug))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

    async def set_user_group_budget(self, ug: UserGroup):
        conn = await self.conn.get_conn()
        sql_update = '''UPDATE user_group 
                    SET user_group_budget = $1
                    WHERE user_id = $2 AND group_id = $3;'''

        sql_select = '''SELECT * FROM user_group 
                            WHERE user_id = $1 AND group_id = $2;'''
        try:
            await conn.execute(sql_update, ug.user_group_budget, ug.user_id, ug.group_id)
        except Exception as e:
            raise Exception(f"Error executing UPDATE: {str(e)}")
        try:
            updated_user_group = await conn.fetchrow(sql_select, ug.user_id, ug.group_id)

            if updated_user_group:
                return UserGroup(**dict(updated_user_group))
            return None
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

