from typing import List

from .card import CardModel
from .user import UserModel

model_metadata: List = [
    CardModel.metadata, UserModel.metadata,
]
