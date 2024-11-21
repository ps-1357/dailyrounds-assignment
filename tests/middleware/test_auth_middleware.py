import pytest
from fastapi import FastAPI, HTTPException
from starlette.testclient import TestClient
from app.middleware.auth_middleware import AuthMiddleware
from unittest.mock import patch


app = FastAPI()

@app.get("/protected")
def protected_endpoint():
    return {"message": "This is protected"}

app.add_middleware(AuthMiddleware)
client = TestClient(app)

def test_protected_endpoint_with_valid_token():
    response = client.get("/protected", headers={"Authorization": "Bearer admin_token_123"})
    assert response.status_code == 200
    assert response.json() == {"message": "This is protected"}