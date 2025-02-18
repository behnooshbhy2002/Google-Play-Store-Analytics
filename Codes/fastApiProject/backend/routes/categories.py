from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import SessionLocal
from backend.models.category_model import Category, CategoryCreate, CategoryResponse
from typing import List

router = APIRouter()

# Dependency for obtaining a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Retrieve all categories
@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# 2. Add a new category
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Check if the category already exists
    db_category = db.query(Category).filter(Category.category_name == category.category_name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
