from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime
    updated_at: datetime
