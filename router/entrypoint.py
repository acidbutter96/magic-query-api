from fastapi import APIRouter
from utils.dotenv import config

router = APIRouter(
    tags=["main"]
)

@router.get("/")
async def root():
    return {
        "application" :"Magic Card Storage Application",
        "version" :config["VERSION"],
    }
