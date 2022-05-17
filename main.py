from fastapi import FastAPI

from router import entrypoint

app = FastAPI()

app.include_router(entrypoint.router)
