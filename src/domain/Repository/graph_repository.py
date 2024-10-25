from ..database import Database
from src.domain.user import User
from src.domain.group import Group
from src.domain.filter import TripFilter

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
                MATCH (n:Estacion)-[r:RUTA*3]->(m:Estacion)
                """

        filters_nodos = []
        filters_rutas = []

        if filtro.ciudad_origen:
            filters_nodos.append(f"n.ciudad = '{filtro.ciudad_origen}'")
        if filtro.ciudad_destino:
            filters_nodos.append(f"m.ciudad = '{filtro.ciudad_destino}'")
        if filtro.pais:
            filters_nodos.append(f"n.pais = '{filtro.pais}'")
        if filtro.tipo_estacion:
            filters_nodos.append(f"r.tipo = '{filtro.tipo_estacion}'")



        if filters_nodos:
            query += "WHERE " + " AND ".join(filters_nodos)


        query += ''' RETURN n, r, m
                LIMIT 2
                  $$) AS result(nodo1 agtype, relacion agtype, nodo2 agtype)'''
        print(query)
        result = await conn.fetch(query)
        return result

    async def maxSetFilterTrip(self):
        '''
            SELECT *
                    FROM cypher(
                    'el_grefo',
                    $$
                    MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
                    WHERE nodo_inicio.ciudad = 'Valencia' AND nodo_fin.ciudad = 'Madrid'
                    UNWIND rel AS r
                    WITH nodo_inicio, nodo_fin, p, SUM(r.distancia) AS total_distancia
                    WHERE total_distancia <= 500
                    RETURN p
                    ORDER BY total_distancia ASC
                    LIMIT 3
                    $$
            ) AS (camino agtype);
            '''


    async def customfilter(self, filter: TripFilter):
        if not GraphRepository.initialized:
            await self.first()
        conn = await self.conn.get_conn()

        consulta = """
            SELECT *
            FROM cypher(
        async def maxSetFilterTrip():
        '''
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
        if filter.tipo_estacion:
            condiciones_estaciones.append(f"nodo_inicio.tipo_estacion = '{filter.tipo_estacion}'")

        # Si hay condiciones de estaciones, las añadimos al primer WHERE
        if condiciones_estaciones:
            consulta += " WHERE " + " AND ".join(condiciones_estaciones)

        # 3. Agregamos el UNWIND y calculamos las sumas en WITH
        consulta += """
                MATCH p = (nodo_inicio:Estacion)-[rel:RUTA*1..5]->(nodo_fin:Estacion)
                WHERE nodo_inicio.id = 6 AND nodo_fin.id = 11
                UNWIND rel AS r
                WITH nodo_inicio, nodo_fin, p,
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

        # Si hay condiciones de rutas, las añadimos al segundo WHERE
        if condiciones_rutas:
            consulta += " WHERE " + " AND ".join(condiciones_rutas)

        # 5. Añadimos el RETURN, ORDER BY y LIMIT
        consulta += """
                WITH nodo_inicio, nodo_fin, p, SUM(r.distancia) AS total_distancia, SUM(r.precio_billete) AS total_precio
                WHERE total_precio <= 300
                RETURN p
                ORDER BY total_distancia ASC
                LIMIT 3
                $$
            ) AS (camino agtype);
            """
        print(consulta)
        result = await conn.fetch(consulta)
        return result
