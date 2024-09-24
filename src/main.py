from fastapi import FastAPI

from exception_handlers import attach_exception_handlers
from users.router import router as user_router
from products.router import router as product_router


app = FastAPI()


app.include_router(user_router)
app.include_router(product_router)

attach_exception_handlers(app)
