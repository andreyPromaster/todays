from api.views import source
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(source.router, prefix="/sources", tags=["sources"])
