from fastapi import APIRouter
from ..controllers import healthy_controller

healthy_router = APIRouter()

tags = ["healthy"]


@healthy_router.get('/', tags=tags, include_in_schema=False)
async def root():
    return healthy_controller.root()


@healthy_router.get('/healthy', tags=tags, include_in_schema=False)
async def healthy():
    return healthy_controller.healthy()


@healthy_router.get('/liveness', tags=tags, include_in_schema=False)
async def liveness():
    return healthy_controller.liveness()
