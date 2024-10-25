from fastapi import APIRouter, HTTPException, status, Depends
from src.infraestructure.jwt_validator import JwtVal

router = APIRouter()
jwt_val = JwtVal()

@router.post("/{email}/{password}")
async def login(email, password):
    return await jwt_val.login(email, password)