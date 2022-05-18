from fastapi import FastAPI

from database import Base, engine
from router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

for r in router:
    app.include_router(r)
