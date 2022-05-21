from datetime import datetime

from pydantic import BaseModel


class CardBase(BaseModel):
    card_name:str | None
    edition:int | None
    price:float | None
    foil:bool | None
    quantity:int

class CardCreate(CardBase):
    ...
class CardUpdate(CardBase):
    updated_at:datetime = datetime.now()

class CardSchema(CardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

