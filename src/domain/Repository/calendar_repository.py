from ..database import Database
from src.domain.user_calendar import UserCalendar, AvDay, UserAvDay

class CalendarRepository:

    def __init__(self):
        self.conn = Database()

    async def add_day(self, free_day: UserCalendar):
        conn = await self.conn.get_conn()
        sql = '''INSERT INTO calendar (user_id, group_id, available_day)
                    VALUES ($1, $2, $3)
                    RETURNING user_id, group_id, available_day;'''
        try:
            f_day = await conn.fetchrow(sql, free_day.user_id, free_day.group_id, free_day.available_day)
            return UserCalendar(**dict(f_day))
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def delete_day(self, free_day: UserCalendar):
        conn = await self.conn.get_conn()
        sql = '''DELETE FROM calendar
                    WHERE user_id = $1 AND group_id = $2 AND available_day = $3
                    RETURNING user_id, group_id, available_day;'''
        try:
            result = await conn.fetchrow(sql, free_day.user_id, free_day.group_id, free_day.available_day)
            if not result:
                return False
            return True
        except Exception as e:
            raise Exception(f"Error : {str(e)}")


    async def get_common_days(self, group_id):
        conn = await self.conn.get_conn()
        sql = '''SELECT
                    available_day,
                    COUNT(DISTINCT user_id) AS num_users
                FROM calendar
                WHERE group_id = $1
                GROUP BY available_day
                ORDER BY num_users DESC;'''
        try:
            result = await conn.fetch(sql, group_id)
            return [AvDay(**dict(cal)) for cal in result]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

        
    async def get_user_days(self, user_id, group_id):
        conn = await self.conn.get_conn()
        sql = '''SELECT user_id, group_id, available_day
                FROM calendar
                WHERE user_id = $1 AND group_id = $2
                ORDER BY available_day;'''
        try:
            result = await conn.fetch(sql, user_id, group_id)
            return [UserCalendar(**dict(cal)) for cal in result]
        except Exception as e:
            raise Exception(f"Error : {str(e)}")
