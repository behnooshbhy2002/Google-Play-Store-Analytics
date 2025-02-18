from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import field_validator, BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.database.connection import SessionLocal
from backend.models.app_model import App, AppCreate, AppResponse
from backend.models.developer_model import Developer, DeveloperCreate, DeveloperResponse
from typing import List

router = APIRouter()

# Dependency for obtaining a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Retrieve the list of applications
@router.get("/", response_model=List[AppResponse])
def get_apps(db: Session = Depends(get_db)):
    return db.query(App).all()


# 2. Add a new application
@router.post("/", response_model=AppResponse)
def create_app(app: AppCreate, db: Session = Depends(get_db)):
    db_app = App(**app.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


# Pydantic model for update request
class AppUpdateRequest(BaseModel):
    price: float
    last_updated: str  # Accept date as a string

    # Convert string date to datetime
    @field_validator("last_updated")
    @classmethod
    def parse_last_updated(cls, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d")  # Convert to datetime
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

# Update app price and last_updated timestamp (Atomic Transaction)
@router.put("/{app_id}/update")
def update_app(app_id: int, update_data: AppUpdateRequest, db: Session = Depends(get_db)):
    try:
        app = db.query(App).filter(App.id == app_id).first()
        dev = db.query(Developer).filter(Developer.developer_id.in_([app.developer_id]))
        # print(dev)

        if not app:
            raise HTTPException(status_code=404, detail="App not found")

        # Validate price
        print(update_data.price)
        if update_data.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")

        # Update fields
        app.price = update_data.price
        app.last_updated = update_data.last_updated  # This is already a valid datetime

        db.commit()  # ✅ No explicit db.begin(), just commit

        return {"message": "App updated successfully", "app_id": app.id}

    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of failure
        print(f"Database error: {str(e)}")  # Debugging
        raise HTTPException(status_code=500, detail="Database error. Transaction rolled back.")
