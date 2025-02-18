from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import SessionLocal
from backend.models.content_ratings_model import ContentRating

router = APIRouter()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_content_ratings(db: Session = Depends(get_db)):
    """Fetch all content ratings"""
    return db.query(ContentRating).all()
