from datetime import datetime

from database.models import UserModel
from database.schemas import UserCreate, UserSchema
from database.schemas.user import UserUpdate
from sqlalchemy.orm import Session


def create_user(db:Session, user: UserCreate)->UserModel:
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

def read_user(db:Session, user_id: int):
    return db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

def read_user_by_username(db:Session, username:str):
    return db.query(UserModel).filter(
        UserModel.username == username
    ).first()

def read_user_by_email(db:Session, email:str):
    return db.query(UserModel).filter(
        UserModel.email == email
    ).first()

def update_user(db:Session, id:int, new_data:UserUpdate):
    if student := read_user(db, id):
        new_data = new_data.dict()
        if 'authentication' in new_data.keys():
            del new_data['authentication']
        new_data["updated_at"] = datetime.now()
        db.query(UserModel).filter(UserModel.id == id).update(new_data)
        db.commit()
        db.refresh(student)
    return student

def delete_user(db:Session, id:int):
    if student := read_user(db, id):
        db.delete(student)
        db.commit()
        return True
    return False
