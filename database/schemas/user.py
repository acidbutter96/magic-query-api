from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime = None
    updated_at: datetime = None

class UserCreate(UserBase):
    is_deleted: bool = False
    is_active: bool = True
    password: str

# class UserStatus(UserBase):
#     ...

class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True

