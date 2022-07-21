from api.views import source, theme, user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(source.router, prefix="/sources", tags=["sources"])
api_router.include_router(theme.router, prefix="/themes", tags=["themes"])
api_router.include_router(user.router, prefix="", tags=["themes"])
