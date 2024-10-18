from fastapi import FastAPI
from ..domain.Repository.user_repository import UserRepository
from src.domain.Repository.group_repository import GroupRepository
from src.domain.Repository.graph_repository import GraphRepository
from uuid import UUID

app = FastAPI()
user_repo = UserRepository()
group_repo = GroupRepository()
graph_repo = GraphRepository()

@app.get("/users")
async def get_all_users():
    users = await user_repo.get_users()
    return users

@app.get("/user/{user_id}")
async def get_user_by_id(user_id: UUID):
    user = await user_repo.get_user_by_id(user_id)
    return user

@app.get("/groups")
async def get_all_groups():
    groups = await group_repo.get_groups()
    return groups


@app.get("/groups/{user_id}")
async def get_groups_by_user(user_id: UUID):
    groups = await group_repo.get_groups_by_user(user_id)
    return groups

@app.get("/users/{group_id}")
async def get_users_by_group(group_id: UUID):
    users = await user_repo.get_users_by_group(group_id)
    return users

@app.get("/prueba")
async def get_grafo():
    grafo =await graph_repo.prueba()
    return grafo