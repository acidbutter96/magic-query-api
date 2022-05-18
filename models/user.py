from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class UserModel(BaseModel):
    id: Optional[UUID] = uuid4()
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime = None
