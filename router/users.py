from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.dotenv import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@users_router.get("/")
async def get_user(token:str=Depends(oauth2_scheme)):
    return {"token":token}

@users_router.get("/users")
async def get_users():
    return {
        "result": "db"
        }
