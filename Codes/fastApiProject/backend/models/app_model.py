from datetime import date

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from backend.database.connection import Base  # Import the database
from pydantic import BaseModel
from typing import Optional


# SQLAlchemy model for the apps table
class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, nullable=False)
    app_id = Column(String(255), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    rating = Column(Float)
    rating_count = Column(Integer)
    installs = Column(Integer)  # BIGINT in SQL maps to Integer in SQLAlchemy
    min_installs = Column(Integer)
    max_installs = Column(Integer)
    is_free = Column(Boolean)
    price = Column(Float)
    currency = Column(String(10))
    size_mb = Column(Float)
    min_android = Column(String(50))
    developer_id = Column(Integer, ForeignKey("developers.id", ondelete="SET NULL"), nullable=True)
    released = Column(Date)
    last_updated = Column(Date)
    content_rating = Column(Integer, ForeignKey("content_ratings.id", ondelete="SET NULL"), nullable=True)
    privacy_policy = Column(String)
    ad_supported = Column(Boolean)
    in_app_purchases = Column(Boolean)
    editors_choice = Column(Boolean)

class AppBase(BaseModel):
    app_name: str
    app_id: str
    category_id: Optional[int] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    installs: Optional[int] = None
    min_installs: Optional[int] = None
    max_installs: Optional[int] = None
    is_free: Optional[bool] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    size_mb: Optional[float] = None
    min_android: Optional[str] = None
    developer_id: Optional[int] = None
    released: Optional[date] = None
    last_updated: Optional[date] = None
    content_rating: Optional[int] = None
    privacy_policy: Optional[str] = None
    ad_supported: Optional[bool] = None
    in_app_purchases: Optional[bool] = None
    editors_choice: Optional[bool] = None


# Request model for creating an app
class AppCreate(AppBase):
    pass


# Response model for returning app details
class AppResponse(AppBase):
    id: int  # Add ID field for responses

    class Config:
        from_attributes = True  # Use SQLAlchemy models as Pydantic sources
