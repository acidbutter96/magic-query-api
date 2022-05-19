
from typing import List

from database.session import Base

from .card import CardModel
from .user import UserModel

model_metadata: List = [
    CardModel.metadata, UserModel.metadata,
]
