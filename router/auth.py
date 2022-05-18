from fastapi import APIRouter, Header, Response, status

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.post("/")
async def get_token(response:Response, app_key: str | None = Header(default=None)):
    ...
