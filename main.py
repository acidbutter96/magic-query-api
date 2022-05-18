from fastapi import FastAPI

from router import router

app = FastAPI()

for r in router:
    app.include_router(r)
