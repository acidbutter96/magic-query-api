from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UserAuthentication(BaseModel):
    username: str
    password: str

class UserUpdate(UserBase):
    authentication: UserAuthentication

class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True

