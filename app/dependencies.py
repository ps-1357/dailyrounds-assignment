# app/dependencies.py

from fastapi import Depends, HTTPException, Request, status
# from app.utils.auth_utils import require_role

async def get_current_user(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user

def require_role(role: str):
    async def role_checker(request: Request):
        print(f"Checking role: {role}")  # Debugging output
        user = getattr(request.state, "user", None)
        if not user or user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return user
    return role_checker


