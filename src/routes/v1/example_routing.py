from controllers import example_controller
from fastapi import APIRouter
from handlers.errors import has_errors

example_router = APIRouter()

tags = ['example']


@example_router.get('/get/{code}', tags=tags)
@has_errors
async def example_get(code: int):
    return example_controller.example_get(code)
