from fastapi import FastAPI
from src.api.routes.api_users import router as users_router
from src.api.routes.api_groups import router as groups_router
from src.api.routes.api_trips import router as trips_router
from src.api.routes.api_login import router as login_router
from src.api.routes.api_user_group import router as user_group_router
from src.api.routes.api_polls import router as polls_router
from src.api.routes.api_calendar import router as calendar_routes
from src.api.routes.api_planning import router as planning_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O ["*"] para permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # O especifica ["GET", "POST", etc.]
    allow_headers=["*"],  # O especifica ["Content-Type", "Authorization", etc.]
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(groups_router, prefix="/groups", tags=["groups"])
app.include_router(trips_router, prefix="/trip", tags=["trip"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(user_group_router, prefix="/user_group", tags=["user_group"])
app.include_router(polls_router, prefix="/polls", tags=["polls"])
app.include_router(calendar_routes, prefix="/calendar", tags=["calendar"])
app.include_router(planning_router, prefix="/api", tags=["planning"])
