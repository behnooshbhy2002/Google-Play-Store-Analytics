from sqlalchemy import Column, Integer, String
from backend.database.connection import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy model
class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    developer_id = Column(String, nullable=False)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)

# Pydantic model for API
class DeveloperBase(BaseModel):
    developer_id: str
    website: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True  # Fix for Pydantic v2

# Model for creating a new Developer
class DeveloperCreate(DeveloperBase):
    pass

# Model for API response
class DeveloperResponse(DeveloperBase):
    id: int
