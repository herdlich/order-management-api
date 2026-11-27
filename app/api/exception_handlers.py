from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.base import NotFoundError, AlreadyExistsError


async def not_found_handler(
        _request: Request,
        exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


async def already_exists_handler(
        _request: Request,
        exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )


def register_exception_handlers(app: FastAPI):
    handlers = {
        NotFoundError: not_found_handler,
        AlreadyExistsError: already_exists_handler,
    }

    for exception, handler in handlers.items():
        app.add_exception_handler(exception, handler)