import asyncpg
import os
from dotenv import load_dotenv
class Database:

    def __init__(self):
        self._conn = None

    async def connect(self):
        load_dotenv()
        self._conn = await asyncpg.connect(
            user=os.getenv('USERDB'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE'),
            host=os.getenv('HOST'),
            port=os.getenv('PORT')
        )

    async def get_conn(self):
        if self._conn is None:
            await self.connect()
        return self._conn
