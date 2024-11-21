from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

MOCK_USERS_DB = [
    {"username": "admin_user", "user_id": "1", "role": "admin", "token": "admin_token_123"},
    {"username": "customer1", "user_id": "2", "role": "customer", "token": "customer_token_123"},
    {"username": "customer2", "user_id": "3", "role": "customer", "token": "customer_token_456"},
    {"username": "customer3", "user_id": "4", "role": "customer", "token": "customer_token_789"},
    {"username": "customer4", "user_id": "5", "role": "customer", "token": "customer_token_321"},
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/openapi.json", "/"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]
        user = next((u for u in MOCK_USERS_DB if u["token"] == token), None)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token or user not found")

        request.state.user = user
        return await call_next(request)