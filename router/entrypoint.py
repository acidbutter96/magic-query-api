from fastapi import APIRouter

router = APIRouter(
    tags=["main"]
)

@router.get("/")
async def root():
    return {
        "application":"Magic Card Storage Application",
        "version": "1.0.0"
    }
