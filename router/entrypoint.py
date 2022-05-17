from fastapi import APIRouter

router = APIRouter(
    tags=["main"]
)

@router.get("/")
async def root():
    return {"message":"teste"}
