from fastapi import FastAPI

from app.features.products import router as product
from app.features.users import router as user
from app.features.carts import router as cart

app = FastAPI(
    title="Order Management API",
    version="beta",
)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(cart.router)