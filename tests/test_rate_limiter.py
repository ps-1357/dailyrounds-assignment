from slowapi.util import get_remote_address
from app.rate_limiter import limiter

def test_rate_limiter_key_function():
    mock_request = type("Request", (object,), {"client": type("Client", (object,), {"host": "127.0.0.1"})()})()
    key = get_remote_address(mock_request)
    assert key == "127.0.0.1"