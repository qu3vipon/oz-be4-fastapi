from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.cache import redis_client
from core.exception_handlers import attach_exception_handlers
from users.router import router as user_router
from users.router_async import router as user_async_router
from products.router import router as product_router


app = FastAPI()


@app.get("/")
def root_handler():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(user_async_router)
app.include_router(product_router)

attach_exception_handlers(app)
