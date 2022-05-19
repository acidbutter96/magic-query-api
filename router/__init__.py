from .routes.auth import auth_router
from .routes.cards import cards_router
from .routes.entrypoint import main_router
from .routes.users import users_router

router = [main_router,auth_router,cards_router,users_router]
