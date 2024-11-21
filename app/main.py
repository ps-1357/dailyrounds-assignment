from fastapi import FastAPI, Request
import logging

from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.security_middleware import SecurityHeadersMiddleware
from app.api.v1 import product_api 

app = FastAPI()

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthMiddleware)


@app.get("/")
async def read_root():
    logging.info("Processing root endpoint")
    return {
        "msg": "Hello World"
    }

app.include_router(product_api.router, prefix="/products", tags=["Products"])
