# Order Management API

REST API for managing users, products, and shopping carts in an online store.

## Features

- User registration and JWT authentication.
- Product creation.
- Adding products to a shopping cart with automatic quantity updates.

Order management is under development.

## Tech Stack

- Python, FastAPI
- PostgreSQL, SQLAlchemy (async)
- Alembic
- Pydantic
- PyJWT

## Database

- `users` — user accounts.
- `products` — product information.
- `carts` — user shopping carts.
- `cart_items` — products added to carts.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/herdlich/order-management-api.git
   cd order-management-api
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create `app/.env` based on `app/.env.example` and configure the PostgreSQL connection and JWT settings. Make sure the database exists.

4. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

5. Start the server:

   ```bash
   uvicorn app.api.api:app --reload
   ```

## API Documentation

Swagger UI: http://127.0.0.1:8000/docs
