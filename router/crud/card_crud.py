from datetime import datetime

from database.models import CardModel
from database.schemas import CardCreate, CardUpdate
from sqlalchemy.orm import Session


def create_card(db:Session, card:CardCreate, user_id:int)->CardModel:
    db_card = CardModel(card_name=card.card_name, edition=card.edition,
                    edition=card.edition, price=card.price,
                    price=card.price, foil=card.foil,
                    quantity=card.quantity, user_id=user_id
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def read_card(db:Session, card_id: int):
    return db.query(CardModel).filter(
        CardModel.id == card_id
    ).first()

def list_cards(db:Session, user_id:int):
    return db.query(CardModel).filter(
        CardModel.user_id == user_id,
    ).all()

def update_card(db:Session, card_id:int, new_data: CardUpdate):
    if card := read_card(db, card_id):
        new_data = new_data.dict()
        new_data["updated_at"] = datetime.now()
        db.query(CardModel).filter(CardModel.id == card_id).update(new_data)
        db.commit()
        db.refresh(card)
    return card

def delete_card(db:Session, id:int):
    if card:= read_card(db, id):
        try:
            db.query(CardModel).filter(CardModel.id == id).delete()
            db.commit()
        except Exception:
            return False
        return True
    return False
