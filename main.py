from fastapi import FastAPI

from database.models import model_metadata
from database.session import Base, engine
from router import router

for meta in model_metadata:
    meta.create_all(bind=engine)

# Base.metadata.create_all(bind=engine)

app = FastAPI()

for r in router:
     app.include_router(r)
