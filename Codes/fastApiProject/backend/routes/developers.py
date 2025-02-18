from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from backend.database.connection import SessionLocal
from backend.models.app_model import App
from pydantic import BaseModel, field_validator

router = APIRouter()

# Dependency for obtaining a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for update request
class AppUpdateRequest(BaseModel):
    price: float
    last_updated: str  # Accept date as a string
    description: str

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
    print(app_id)
    try:
        app = db.query(App).filter(App.id == app_id).first()
        print(f"App Found: {app}")  # Debugging

        if not app:
            return
            # raise HTTPException(status_code=404, detail="App not found")

        # Validate price
        if update_data.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")

        # Begin transaction
        with db.begin():
            app.price = update_data.price
            app.description = update_data.description
            app.last_updated = update_data.last_updated  # Now it's a valid datetime
            db.commit()  # Commit transaction

        return {"message": "App updated successfully", "app_id": app.id}

    except SQLAlchemyError:
        db.rollback()  # Rollback if any error occurs
        raise HTTPException(status_code=500, detail="Database error. Transaction rolled back.")
