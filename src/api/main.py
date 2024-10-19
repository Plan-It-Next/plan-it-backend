from fastapi import FastAPI
from src.api.routes.api_users import router as users_router
from src.api.routes.api_groups import router as groups_router
from src.api.routes.api_trips import router as trips_router


app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(groups_router, prefix="/groups", tags=["groups"])
app.include_router(trips_router, prefix="/trip", tags=["trip"])


