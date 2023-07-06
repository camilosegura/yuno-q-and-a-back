from os import getenv
from fastapi import APIRouter
from .healthy import healthy_router
from .v1 import api_v1

routes = APIRouter()

_PREFIX_PATH = getenv("PREFIX_PATH", "/prefix")

routes.include_router(healthy_router, prefix=_PREFIX_PATH)
routes.include_router(router=api_v1, prefix=f'{_PREFIX_PATH}/v1')
