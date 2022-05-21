from database import get_db
from database.crud import user_crud
# from database.models import UserModel
from database.schemas import UserCreate, UserSchema, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from utils.dotenv import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@users_router.post("/")
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
    
    created = user_crud.create_user(db=db, user=user)
    return {
        "status": "User registered successfully",
    }

@users_router.get("/", response_model=UserSchema)
def read_get_user(db:Session = Depends(get_db)):
    # recover id from jwt
    id = 1
    return user_crud.read_user(db, id)

@users_router.get("/users")
async def read_get_users():
    return {
        "result": "db"
        }

@users_router.put("/", response_model=UserSchema)
def put_update_user(new_user:UserUpdate, db:Session = Depends(get_db)):
    # token is valid - get user id
    # validate password
    id = 1
    if db_user := user_crud.update_user(db, id, new_user):
        return db_user

@users_router.delete("/")
def delete_delete_user(db:Session = Depends(get_db)):
    id = 3
    if db_user:= user_crud.read_user(db, id):
        if user_crud.delete_user(db, id) and not db_user.deleted_at:
            return {"info": f"user_id: {id} was deleted successfully."}
        else:
            raise HTTPException(status_code=500, detail={
            "status": "User cannot be deleted"
        })
    raise HTTPException(
        status_code=400,
        detail={"status":"There's no such user with the specified id, probably the user already was deleted."}
        )
