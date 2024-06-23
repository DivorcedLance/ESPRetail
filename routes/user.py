from fastapi import APIRouter

user = APIRouter()

@user.get("/")
async def get_users():
    return {"message": "Get all users"}

