from fastapi import FastAPI

from database import SessionLocal, engine, models
from router import router

for meta in models.model_metadata:
    meta.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

for r in router:
    app.include_router(r)
