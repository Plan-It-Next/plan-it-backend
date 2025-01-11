from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.api_users import router as users_router
from src.api.routes.api_groups import router as groups_router
from src.api.routes.api_trips import router as trips_router
from src.api.routes.api_login import router as login_router
from src.api.routes.api_user_group import router as user_group_router
from src.api.routes.api_polls import router as polls_router
from src.api.routes.api_calendar import router as calendar_routes

app = FastAPI()

origins = [
    "http://localhost:3001",  # Permitir solicitudes desde el frontend
    "http://127.0.0.1:3001", # También permitir desde 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(groups_router, prefix="/groups", tags=["groups"])
app.include_router(trips_router, prefix="/trip", tags=["trip"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(user_group_router, prefix="/user_group", tags=["user_group"])
app.include_router(polls_router, prefix="/polls", tags=["polls"])
app.include_router(calendar_routes, prefix="/calendar", tags=["calendar"])

