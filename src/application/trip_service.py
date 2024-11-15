import json
import re
from src.domain.Repository.graph_repository import GraphRepository
from src.domain.filter import TripFilter

graph_repo = GraphRepository()

class TripService():

    async def get_grafo(self):
        grafo = await graph_repo.prueba()
        return grafo

    async def get_viaje_filtro(self,filtro: TripFilter):
        viaje = await graph_repo.trip_filter(filtro)
        return viaje

    async def get_trip_custom_filters(self, filter: TripFilter):
        trip=  await graph_repo.customfilter(filter)
        print(trip)
        trip_format = await self.formatear_resultado_caminos(trip)
        return trip_format


    async def formatear_resultado_caminos(self,resultados_json):
        caminos_formateados = []

        # Itera sobre cada resultado (camino) en el JSON
        for resultado in resultados_json:
            json_string = re.sub(r'::(vertex|edge|path)', '', resultado["camino"])
            camino = json.loads(json_string)  # Convierte el string JSON del camino a objeto
            viaje = []

            # Itera sobre los elementos en el camino, agrupando estaciones y rutas
            for elemento in camino:
                if elemento["label"] == "Estacion":
                    estacion = {
                        "id": elemento["id"],
                        "nombre": elemento["properties"]["nombre"],
                        "ciudad": elemento["properties"]["ciudad"],
                        "latitud": elemento["properties"]["latitud"],
                        "longitud": elemento["properties"]["longitud"]
                    }
                    viaje.append({"tipo": "estacion", "detalles": estacion})
                elif elemento["label"] == "RUTA":
                    ruta = {
                        "id": elemento["id"],
                        "tipo": elemento["properties"]["tipo"],
                        "duracion": elemento["properties"]["duracion"],
                        "distancia": elemento["properties"]["distancia"],
                        "precio_billete": elemento["properties"]["precio_billete"],
                        "fecha_hora_salida": elemento["properties"]["fecha_hora_salida"],
                        "fecha_hora_llegada": elemento["properties"]["fecha_hora_llegada"]
                    }
                    viaje.append({"tipo": "ruta", "detalles": ruta})

            # Añade el viaje ya formateado a la lista de caminos
            caminos_formateados.append(viaje)

        return caminos_formateados



