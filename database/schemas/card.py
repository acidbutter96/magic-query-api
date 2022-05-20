from datetime import datetime

from pydantic import BaseModel


class CardBase(BaseModel):
    card_name:str
    edition:int
    price:float
    foil:bool
    quantity:int
    user_id: int

class CardCreate(CardBase):
    ...
class CardUpdate(CardBase):
    updated_at:datetime = datetime.now()

class CardSchema(CardBase):
    id: int

    class Config:
        orm_mode = True

