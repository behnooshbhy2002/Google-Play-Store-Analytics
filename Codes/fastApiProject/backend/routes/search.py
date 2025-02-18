from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
from backend.database.connection import SessionLocal
from backend.models.app_model import App
from backend.models.category_model import Category
from backend.models.content_ratings_model import ContentRating
from dataclasses import asdict

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def search_apps(
    category_name: list[str] = Query([]),
    content_rating: list[str] = Query([]),
    min_rating: float = 0.0,
    max_rating: float = 5.0,
    min_price: float = 0.0,
    max_price: float = 100.0,
    app_name: str = "",
    sort_by: str = "rating",
    sort_order: str = "desc",
    show_execution_time: bool = False,
    db: Session = Depends(get_db),
):
    print("Received categories:", category_name)
    print("Received content ratings:", content_rating)

    if max_price < min_price:
        max_price = float("inf")

    # Step 1: Build the base query (without indexing)
    query = db.query(App)

    # Apply filters to the query
    if category_name:
        category_ids = [cat.id for cat in db.query(Category).filter(Category.category_name.in_(category_name)).all()]
        query = query.filter(App.category_id.in_(category_ids))

    if content_rating:
        content_rating_ids = [cr.id for cr in db.query(ContentRating).filter(ContentRating.content_rating.in_(content_rating)).all()]
        query = query.filter(App.content_rating.in_(content_rating_ids))

    query = query.filter(App.rating.between(min_rating, max_rating))

    if max_price == float("inf"):
        query = query.filter(App.price >= min_price)
    else:
        query = query.filter(App.price.between(min_price, max_price))

    if app_name:
        query = query.filter(App.app_name.ilike(f"%{app_name}%"))

    # Apply sorting
    if sort_by == "category":
        query = query.join(Category).order_by(
            Category.category_name.asc() if sort_order == "asc" else Category.category_name.desc())
    elif sort_by == "rating":
        query = query.order_by(App.rating.asc() if sort_order == "asc" else App.rating.desc())
    elif sort_by == "price":
        query = query.order_by(App.price.asc() if sort_order == "asc" else App.price.desc())



    if show_execution_time:
        # Step 2: Execute the query and EXPLAIN ANALYZE **before indexing**
        compiled_query = query.statement.compile(db.bind, compile_kwargs={"literal_binds": True})
        print(str(compiled_query))
        explain_query_before = f"EXPLAIN ANALYZE {str(compiled_query)}"

        try:
            db.execute(text("DROP INDEX IF EXISTS idx_app_category;"))
            # db.execute(text("DROP INDEX IF EXISTS idx_app_content_rating;"))
            # db.execute(text("DROP INDEX IF EXISTS idx_app_rating_range;"))
            # db.execute(text("DROP INDEX IF EXISTS idx_app_price;"))
            # Execute EXPLAIN ANALYZE before indexing
            explain_result_before = db.execute(text(explain_query_before)).fetchall()
            explain_result_before = [str(row) for row in explain_result_before]  # Convert to strings for JSON serialization
        except Exception as e:
            explain_result_before = str(e)  # Fallback in case of errors


        # Step 4: Execute the query and EXPLAIN ANALYZE **after indexing**
        try:
            # Recompile the query (in case the index affects the execution plan)
            compiled_query = query.statement.compile(db.bind, compile_kwargs={"literal_binds": True})
            explain_query_after = f"EXPLAIN ANALYZE {str(compiled_query)}"

            # Execute EXPLAIN ANALYZE after indexing
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_app_category ON apps (category_id);"))
            # db.execute(text("CREATE INDEX IF NOT EXISTS idx_app_content_rating ON apps (content_rating);"))
            # db.execute(text("CREATE INDEX IF NOT EXISTS idx_app_rating_range ON apps (rating);"))
            # db.execute(text("CREATE INDEX IF NOT EXISTS idx_app_price ON apps (price);"))
            explain_result_after = db.execute(text(explain_query_after)).fetchall()
            explain_result_after = [str(row) for row in explain_result_after]  # Convert to strings for JSON serialization
        except Exception as e:
            explain_result_after = str(e)  # Fallback in case of errors
    else:
        explain_result_before = []
        explain_result_after = []

    # Step 5: Fetch the actual results (after indexing)
    results = query.distinct().all()

    # print(explain_result_before, explain_result_after)
    return {
        "results": results,
        "explain_before_indexing": explain_result_before,
        "explain_after_indexing": explain_result_after,
    }


