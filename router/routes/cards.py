from database import get_db
from database.crud import card_crud, user_crud
from database.schemas import CardCreate, CardSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

cards_router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@cards_router.post("/create", response_model=CardSchema)
def post_create_card(card:CardCreate, db:Session = Depends(get_db)):
    id = 1
    if db_user := user_crud.read_user(db, id):
        if db_card := card_crud.read_card_by_name(db, id, card.card_name):
            card_id = db_card.card_id
            new_card = card_crud.update_card(db, card_id, {
                "quantity": db_card.quantity + card.quantity,
                })
            return new_card
    else:
        raise HTTPException(status_code=400,
        detail={
            "status": "User not founded"
        }
        )
    new_card = card_crud.create_card(db, card, id)
    return new_card
