from fastapi import APIRouter
from src.domain.Repository.graph_repository import GraphRepository
from src.application.trip_service import TripService
from src.domain.filter import TripFilter
from uuid import UUID

router = APIRouter()
graph_repo = GraphRepository()
trip_service = TripService()

@router.get("/")
async def get_grafo():
    grafo =await trip_service.prueba()
    return grafo

@router.post("/viaje_filtro")
async def get_viaje_filtro(filtro: TripFilter):
    viaje = await trip_service.trip_filter(filtro)
    return viaje

@router.post("/trip_last_filter")
async def get_trip_filter(filter: TripFilter):
    trip = await trip_service.get_trip_custom_filters(filter)
    return trip