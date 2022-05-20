from database import get_db
from database.models import UserModel
from database.schemas import UserCreate, UserSchema, UserUpdate
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
def post_create_user(user:UserCreate, db:Session = Depends(get_db)):
    if db_user_email := user_crud.read_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail={
            "status":"The email is already registered, try another one"
            }
        )

    if db_user_username := user_crud.read_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail={
            "status": "User already exists"
        })

    return user_crud.create_user(db=db, user=user)

@users_router.get("/")
async def read_get_user(token:str=Depends(oauth2_scheme)):
    return {"token":token}

@users_router.get("/users")
async def read_get_users():
    return {
        "result": "db"
        }

@users_router.put("/", response_model=UserSchema)
def put_update_user(new_user:UserUpdate, db:Session = Depends(get_db)):
    print(f"Password {new_user}\nusername: {new_user.username}")
    # token is valid - get user id
    # validate password
    id = 1
    if db_user := user_crud.update_user(db, id, new_user):
        return db_user

