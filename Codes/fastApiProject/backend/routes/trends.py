from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from backend.database.connection import SessionLocal
from backend.models.app_model import App
from backend.models.category_model import Category

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/releases-per-year")
def get_releases_per_year(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_name == category_name).first()
    if not category:
        return {"error": "Category not found"}

    releases = (
        db.query(func.extract('year', App.released).label("year"), func.count().label("count"))
        .filter(App.category_id == category.id, App.released.isnot(None))
        .group_by("year")
        .order_by("year")
        .all()
    )
    return [{"year": int(year), "count": count} for year, count in releases if year is not None]

@router.get("/updates-per-year")
def get_updates_per_year(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_name == category_name).first()
    if not category:
        return {"error": "Category not found"}

    updates = (
        db.query(func.extract('year', App.last_updated).label("year"), func.count().label("count"))
        .filter(App.category_id == category.id, App.last_updated.isnot(None))
        .group_by("year")
        .order_by("year")
        .all()
    )
    return [{"year": int(year), "count": count} for year, count in updates if year is not None]

@router.get("/rating-distribution")
def get_rating_distribution(db: Session = Depends(get_db)):
    ratings = (
        db.query(
            func.width_bucket(App.rating, 1, 5, 20).label("bin"),
            func.count().label("count")
        )
        .filter(App.rating.isnot(None))
        .group_by("bin")
        .order_by("bin")
        .all()
    )
    return [{"bin": (bin - 1) * 0.2 + 1, "count": count} for bin, count in ratings]


@router.get("/avg-rating-per-category")
def get_avg_rating_per_category(db: Session = Depends(get_db)):
    query = text("""
            SELECT category_name, avg_rating, total_apps
            FROM avg_rating_per_category
        """)

    results = db.execute(query).fetchall()

    return [
        {"category_name": row[0], "avg_rating": row[1], "total_apps": row[2]}
        for row in results
    ]
