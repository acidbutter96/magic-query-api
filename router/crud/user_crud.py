from database.models import UserModel
from database.schemas import UserCreate, UserSchema
from sqlalchemy.orm import Session


def get_user(db:Session, user_id: int):
    return db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

def get_user_by_username(db:Session, username:str):
    return db.query(UserModel).filter(
        UserModel.username == username
    ).first()

def get_user_by_email(db:Session, email:str):
    return db.query(UserModel).filter(
        UserModel.email == email
    ).first()

def create_user(db:Session, user: UserCreate):
    # TODO - authorization scheme
    password = user.password+"fakehash"
    db_user = UserModel(username=user.username, email=user.email,
            first_name=user.first_name, last_name=user.last_name,
            password=password, is_deleted=user.is_deleted,
            is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

