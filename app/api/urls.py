from fastapi import APIRouter
from views import source

api_router = APIRouter()

api_router.include_router(source.router, prefix="/sources", tags=["sources"])
