from app.database import client

def test_database_connection():
    assert client is not None
