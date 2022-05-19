from database import get_db
from database.schemas import UserCreate, UserSchema
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from router.crud import user_crud
from sqlalchemy.orm import Session
from utils.dotenv import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@users_router.post("/", response_model=UserSchema)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    db_user_email = user_crud.get_user_by_email(db, user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail={
            "status":"The email is already registered, try another one"
            }
        )
    db_user_username = user_crud.get_user_by_username(db, user.username)
    if db_user_username:
        raise HTTPException(status_code=400, detail={
            "status": "User already exists"
        })
    return user_crud.create_user(db=db, user=user)

@users_router.get("/")
async def get_user(token:str=Depends(oauth2_scheme)):
    return {"token":token}

@users_router.get("/users")
async def get_users():
    return {
        "result": "db"
        }

