import database.session as data
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.sql import func


class CardModel(data.Base):
    __tablename__ = "cards"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    card_name = Column(String(100), nullable=False)
    edition = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    foil = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, nullable=False,
        server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True),
        onupdate=func.now()
    )
