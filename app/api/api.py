from fastapi import FastAPI

from app.features.users import router as user

app = FastAPI(
    title="Order Management API",
    version="beta",
)

app.include_router(user.router)