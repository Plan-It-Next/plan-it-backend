import csv
import asyncpg
import os
from dotenv import load_dotenv


def escapar_cadena(valor):
    """Escapa comillas simples y otros caracteres en una cadena."""
    return valor.replace("'", "\\'")

async def cargar_estaciones_desde_csv(conn, archivo_csv):
    # Lee el CSV y construye la consulta Cypher
    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        estaciones = []
        id_counter = 1  # Usarás IDs únicos para las estaciones

        for row in reader:
            estaciones.append(f"""
                (n{id_counter}:Estacion {{
                    id: {id_counter},
                    nombre: '{escapar_cadena(row['name'])}',
                    ciudad: '{escapar_cadena(row['city'])}',
                    pais: '{escapar_cadena(row['country'])}',
                    latitud: {row['lat']},
                    longitud: {row['lon']}
                }})
            """)
            id_counter += 1

        # Combina todas las estaciones en una sola consulta CREATE
        query = f"""
        CREATE EXTENSION IF NOT EXISTS age;
        LOAD 'age';
        SET search_path = ag_catalog, "$user", public;
        

        SELECT * FROM cypher('el_grefo', $$
        CREATE
        {','.join(estaciones)}
        $$) AS (n agtype);
        """

        # Ejecuta la consulta
        await conn.execute(query)
        print("Estaciones cargadas exitosamente.")



async def insertar_aristas_desde_csv(conn, ruta_csv):
    # Crear la extensión de AGE si no existe
    await conn.execute('''
        CREATE EXTENSION IF NOT EXISTS age;
        LOAD 'age';
        SET search_path = ag_catalog, "$user", public;
    ''')

    # Plantilla de la consulta Cypher
    query_template = """
    SELECT * FROM cypher('el_grefo', $$
    MATCH (origen:Estacion {ciudad: $1}), (destino:Estacion {ciudad: $2})
    CREATE (origen)-[:RUTA {
        id: $3,
        tipo: $4,
        fecha_hora_salida: $5,
        fecha_hora_llegada: $6,
        precio_billete: $7,
        duracion: $8
    }]->(destino)
    $$) AS (resultado text);
    """

    # Leer el archivo CSV
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        arista_id = 1  # Contador para el ID de las aristas
        for fila in lector:
            # Extraer los datos de la fila
            ciudad_origen = escapar_cadena(fila["ciudad_origen"])
            ciudad_destino = escapar_cadena(fila["ciudad_destino"])
            fecha_salida = fila["hora_salida"]
            fecha_llegada = fila["hora_llegada"]
            duracion = float(fila["duracion_viaje"])
            precio = float(fila["precio"])
            tipo = fila["tipo"]

            # Construcción de la consulta Cypher con los parámetros directamente
            query = f"""
                        SELECT * FROM cypher('el_grefo', $$ 
                        MATCH (origen:Estacion {{ciudad: '{ciudad_origen}'}}), (destino:Estacion {{ciudad: '{ciudad_destino}'}})
                        CREATE (origen)-[:RUTA {{
                            id: {arista_id},
                            tipo: '{tipo}',
                            fecha_hora_salida: '{fecha_salida}',
                            fecha_hora_llegada: '{fecha_llegada}',
                            precio_billete: {precio},
                            duracion: {duracion}
                        }}]->(destino)
                        $$) AS (n agtype);
                        """

            # Ejecutar la consulta para crear la arista
            await conn.execute(query)
            arista_id += 1  # Incrementar el ID de la arista
            if arista_id == 1000:
                print(arista_id)

            if arista_id == 10000:
                print(arista_id)

            if arista_id == 20000:
                print(arista_id)

    print("Rutas cargadas exitosamente.")


async def insertar_aristas_desde_csv2(conn, ruta_csv):
    await conn.execute('''CREATE EXTENSION IF NOT EXISTS age;
        LOAD 'age';
        SET search_path = ag_catalog, "$user", public;''')

    batch_size = 1000  # Definir el tamaño del lote
    batch = []  # Lista para almacenar las consultas por lote
    arista_id = 1

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        contador = 1
        for fila in lector:
            ciudad_origen = fila["ciudad_origen"]
            ciudad_destino = fila["ciudad_destino"]
            fecha_salida = fila["hora_salida"]
            fecha_llegada = fila["hora_llegada"]
            duracion = float(fila["duracion_viaje"])
            precio = float(fila["precio"])
            tipo = fila["tipo"]

            query = f"""
            MATCH (origen:Estacion {{ciudad: '{ciudad_origen}'}}), (destino:Estacion {{ciudad: '{ciudad_destino}'}})
            CREATE (origen)-[:RUTA {{
                id: {arista_id},
                tipo: '{tipo}',
                fecha_hora_salida: '{fecha_salida}',
                fecha_hora_llegada: '{fecha_llegada}',
                precio_billete: {precio},
                duracion: {duracion}
            }}]->(destino)
            """

            batch.append(query)
            arista_id += 1

            # Ejecutar el lote cada `batch_size` consultas
            if len(batch) >= batch_size:
                await conn.execute('SELECT cypher($$ ' + " $$), $$".join(batch) + ' $$) AS c;')
                batch = []  # Limpiar el lote
                print('batch cargado')

    # Ejecutar cualquier consulta restante si no llega al tamaño del lote
    if batch:
        await conn.execute('SELECT cypher($$ ' + " $$), $$".join(batch) + ' $$) AS c;')

    print("Rutas cargadas exitosamente.")



# Configuración de conexión
async def main():
    load_dotenv()
    conn = await asyncpg.connect(
        user=os.getenv('USERDB'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT')
    )
    try:
        await cargar_estaciones_desde_csv(conn, 'estaciones_aeropuertos.csv')
        await insertar_aristas_desde_csv(conn, 'viajes.csv')
    finally:
        await conn.close()


# Ejecutar la función principal
import asyncio

asyncio.run(main())
