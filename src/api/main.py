import requests
from fastapi import FastAPI
from ..domain.Repository.user_repository import User_repository

app = FastAPI()
user_repo = User_repository()

@app.get("/users")
async def get_users():
    users = await user_repo.get_user()
    return users