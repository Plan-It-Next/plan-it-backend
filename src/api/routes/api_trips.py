from fastapi import APIRouter
from src.domain.Repository.graph_repository import GraphRepository
from src.domain.filter import TripFilter
from uuid import UUID

router = APIRouter()
graph_repo = GraphRepository()

@router.get("/")
async def get_grafo():
    grafo =await graph_repo.prueba()
    return grafo

@router.post("/viaje_filtro")
async def get_viaje_filtro(filtro: TripFilter):
    viaje = await graph_repo.trip_filter(filtro)
    return viaje