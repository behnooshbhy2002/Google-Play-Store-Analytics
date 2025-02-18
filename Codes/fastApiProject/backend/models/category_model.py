from sqlalchemy import Column, Integer, String
from backend.database.connection import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy model for the database
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)

# Pydantic model for sending and receiving data in the API
class CategoryBase(BaseModel):
    category_name: str

    class Config:
        from_attributes = True  # Enable ORM support in Pydantic v2

# Model for creating a new category
class CategoryCreate(CategoryBase):
    pass

# Model for API response
class CategoryResponse(CategoryBase):
    id: int
