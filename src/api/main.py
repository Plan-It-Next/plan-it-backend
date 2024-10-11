from fastapi import FastAPI
from ..domain.Repository.user_repository import User_repository

app = FastAPI()
user_repo = User_repository()

@app.get("/users")
async def get_users():
    users = await user_repo.get_user()
    return users

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    user = await user_repo.get_user_by_id(user_id)
    return user