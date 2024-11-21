from bleach import clean
from starlette.middleware.base import BaseHTTPMiddleware

def sanitize_input(input_text: str):
    """Sanitize user input to prevent XSS."""
    return clean(input_text, tags=[], attributes={}, protocols=[])

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add secure HTTP headers."""
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response