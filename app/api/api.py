from fastapi import FastAPI

from app.api.routes import user

app = FastAPI(
    title="Order Management API",
    version="beta",
)

app.include_router(user.router)