from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from pyparsing import Optional


class UserModel(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime = None
