from sqlalchemy import Column, Integer, String
from backend.database.connection import Base  # Import the database

# SQLAlchemy model for the content_ratings table
class ContentRating(Base):
    __tablename__ = "content_ratings"

    id = Column(Integer, primary_key=True, index=True)
    content_rating = Column(String(50), unique=True, nullable=False)
