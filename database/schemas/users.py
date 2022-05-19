from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserStatus(UserBase):
    is_deleted: bool
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
class UserSchema(UserStatus):
    id: int

    class Config:
        orm_mode = True

