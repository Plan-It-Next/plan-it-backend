from ..database import Database
from src.domain.user import User
from src.domain.group import Group
from src.domain.filter import TripFilter
import csv

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


    async def trip_filter(self, filtro: TripFilter):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()

        query = """
        SELECT *
                FROM cypher('el_grefo', $$
                MATCH (n:Estacion)-[r:RUTA]->(m:Estacion)
                """

        filters_nodos = []
        filters_rutas = []

        if filtro.ciudad_origen:
            filters_nodos.append(f"n.ciudad = '{filtro.ciudad_origen}'")
        if filtro.ciudad_destino:
            filters_nodos.append(f"m.ciudad = '{filtro.ciudad_destino}'")
        if filtro.pais:
            filters_nodos.append(f"n.pais = '{filtro.pais}'")
        if filtro.tipo_ruta:
            filters_nodos.append(f"r.tipo = '{filtro.tipo_ruta}'")



        if filters_nodos:
            query += "WHERE " + " AND ".join(filters_nodos)


        query += ''' RETURN n, r, m
                LIMIT 2
                  $$) AS result(nodo1 agtype, relacion agtype, nodo2 agtype)'''
        print(query)
        result = await conn.fetch(query)
        return result

    async def maxSetFilterTrip(self):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()
        query ="""
            SELECT *
            FROM cypher(
                'el_grefo',
                $$
                MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..3]->(nodo_fin:Estacion)
             WHERE nodo_inicio.ciudad = 'Sevilla' AND nodo_fin.ciudad = 'Sevilla'
                UNWIND rel AS r
                WITH nodo_inicio, nodo_fin, r, p,
                     SUM(r.distancia) AS total_distancia,
                     SUM(r.precio_billete) AS total_precio,
                     SUM(r.duracion) AS total_duracion
                WHERE r.tipo = 'metro'
                RETURN p
                ORDER BY total_distancia ASC
                LIMIT 3
                $$
            ) AS (camino agtype);
            """
        result = await conn.fetch(query)
        return result

    async def customfilter(self, filter: TripFilter):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()
        consulta = """
            SELECT *
            FROM cypher(
                'el_grefo',
                $$
                MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..3]->(nodo_fin:Estacion)
            """

        # 2. Construimos el primer WHERE con los filtros de estaciones
        condiciones_estaciones = []
        if filter.ciudad_origen:
            condiciones_estaciones.append(f"nodo_inicio.ciudad = '{filter.ciudad_origen}'")
        if filter.ciudad_destino:
            condiciones_estaciones.append(f"nodo_fin.ciudad = '{filter.ciudad_destino}'")
        if filter.pais:
            condiciones_estaciones.append(f"nodo_inicio.pais = '{filter.pais}'")


        # Si hay condiciones de estaciones, las añadimos al primer WHERE
        if condiciones_estaciones:
            consulta += " WHERE " + " AND ".join(condiciones_estaciones)

        # 3. Agregamos el UNWIND y calculamos las sumas en WITH
        consulta += """
                UNWIND rel AS r
                WITH nodo_inicio, nodo_fin, r, p,
                     SUM(r.distancia) AS total_distancia,
                     SUM(r.precio_billete) AS total_precio,
                     SUM(r.duracion) AS total_duracion
            """

        # 4. Construimos el segundo WHERE con los filter de rutas
        condiciones_rutas = []
        if filter.precio_billete is not None:
            condiciones_rutas.append(f"total_precio <= {filter.precio_billete}")
        if filter.distancia is not None:
            condiciones_rutas.append(f"total_distancia <= {filter.distancia}")
        if filter.duracion is not None:
            condiciones_rutas.append(f"total_duracion <= {filter.duracion}")
        if filter.tipo_ruta:
            condiciones_rutas.append(f"r.tipo = '{filter.tipo_ruta}'")
        if filter.fecha:
            condiciones_rutas.append(f"r.dia = '{filter.fecha}'")

        # Si hay condiciones de rutas, las añadimos al segundo WHERE
        if condiciones_rutas:
            consulta += " WHERE " + " AND ".join(condiciones_rutas)

        # 5. Añadimos el RETURN, ORDER BY y LIMIT
        consulta += """
                RETURN p
                ORDER BY total_distancia ASC
                LIMIT 3
                $$
            ) AS (camino agtype);
            """
        print(consulta)
        result = await conn.fetch(consulta)
        return result

    async def insertNodes(self):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()
        async with conn.transaction():
            async with open('src/estaciones_aeropuertos.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    query = f"""
                       SELECT * FROM cypher('el_grefo', $$
                       CREATE (:Estacion {{
                           id: {row['id']},
                           nombre: '{row['name']}',
                           ciudad: '{row['city']}',
                           pais: '{row['country']}',
                           latitud: {row['lat']},
                           longitud: {row['lon']}
                       }})
                       $$) AS (n agtype);
                       """
                    await conn.execute(query)


    async def get_all_stations(self):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()


        sql = '''
        SELECT *
                FROM cypher('el_grefo', $$
                    MATCH (n)
                    RETURN n
                $$) AS result(nodo1 agtype);'''
        try:
            #await conn.fetch(sql)
            #await conn.fetch(sql12)
            #await conn.fetch(sql13)
            prueba23 = await conn.fetch(sql)

            return prueba23
        except Exception as e:
            raise Exception(f"Error : {str(e)}")

