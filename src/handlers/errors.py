from functools import wraps
from fastapi import HTTPException


def has_errors(f):
    @wraps(f)
    async def executer(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as exc:
            if isinstance(exc, Exception):
                raise HTTPException(status_code=400,
                                    detail=str(exc))
            else:
                raise HTTPException(status_code=500,
                                    detail="Unexpected error")
    return executer
