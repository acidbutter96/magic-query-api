from datetime import datetime
from typing import List

from pydantic import BaseModel

from .card import CardSchema


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_deleted: bool = False
    is_active: bool = True


class UserAuthentication(BaseModel):
    username: str
    password: str

class UserUpdate(UserBase):
    authentication: UserAuthentication

class UserSchema(UserBase):
    id: int
    deleted_at: datetime = None

    class Config:
        orm_mode = True

