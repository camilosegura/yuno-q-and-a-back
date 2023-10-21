from fastapi import APIRouter
from .example_routing import example_router

api_v1 = APIRouter()

api_v1.include_router(prefix="/assistant", router=example_router)
