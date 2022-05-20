from datetime import datetime
from typing import Optional

# from pydantic import BaseModel
from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

# from uuid import UUID, uuid4


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String(10), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    is_deleted = Column(Boolean(create_constraint=False, ), nullable=False)
    is_active = Column(Boolean(create_constraint=True, ), nullable=False)
    deleted_at = Column(DateTime(timezone=True),nullable=True,
                        server_default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
