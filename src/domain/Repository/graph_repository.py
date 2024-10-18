from ..database import Database
from src.domain.user import User
from src.domain.group import Group

class GraphRepository:
    initialized = False

    def __init__(self):
        self.conn = Database()


    async def first(self):
        conn = await self.conn.get_conn()
        sql = '''
                        CREATE EXTENSION IF NOT EXISTS age;'''
        sql12 = '''
                        LOAD 'age';'''
        sql13 = '''
                        SET search_path = ag_catalog, "$user", public;'''
        await conn.fetch(sql)
        await conn.fetch(sql12)
        await conn.fetch(sql13)

        GraphRepository.initialized = True

    async def prueba(self):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()


        sql = '''
        SELECT *
                FROM cypher('el_grefo', $$
                    MATCH (n)
                    OPTIONAL MATCH (n)-[r]->(m)
                    RETURN n, r, m
                $$) AS result(nodo1 agtype, relacion agtype, nodo2 agtype);'''
        try:
            #await conn.fetch(sql)
            #await conn.fetch(sql12)
            #await conn.fetch(sql13)
            prueba23 = await conn.fetch(sql)

            return prueba23
        except Exception as e:
            raise Exception(f"Error : {str(e)}")