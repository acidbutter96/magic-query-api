from .auth import auth_router
from .cards import cards_router
from .entrypoint import main_router
from .users import users_router

router = [main_router,auth_router,cards_router,users_router]
