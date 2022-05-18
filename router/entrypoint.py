from fastapi import APIRouter
from utils.dotenv import config

main_router = APIRouter(
    tags=["main"]
)

@main_router.get("/")
async def root():
    return {
        "application" :"Magic Card Storage Application",
        "version" :config["VERSION"],
    }
