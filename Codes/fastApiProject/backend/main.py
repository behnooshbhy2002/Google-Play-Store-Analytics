from fastapi import FastAPI
from backend.routes import apps, search, trends, developers, categories, content_ratings
from backend.database.connection import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(apps.router, prefix="/apps")
app.include_router(search.router, prefix="/search")
app.include_router(trends.router, prefix="/trends")
app.include_router(developers.router, prefix="/developers")
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(content_ratings.router, prefix="/content_ratings", tags=["Content Ratings"])  # ✅ New Route



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
