# tests/test_products.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from bson import ObjectId

from app.main import app


# Create a TestClient for testing
client = TestClient(app)

headers1= {'Authorization': 'Bearer admin_token_123'}
headers2= {'Authorization': 'Bearer customer_token_789'}

# Test case for creating a product successfully by an admin
def test_create_product_success():

    with patch('app.database.product_collection.insert_one', new_callable=AsyncMock) as mock_insert_one:
        mock_insert_one.return_value.inserted_id = "mock_product_id"

        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 10.99,
            "category": "Test Category",
            "inventory_count": 100 
        }
        
        response = client.post("/products/", json=product_data, headers=headers1)


        assert response.status_code == 200
        assert response.json() == {"message": "Product created", "product_id": "mock_product_id"}
        mock_insert_one.assert_called_once()

def test_create_product_non_admin():
    # Override dependency to simulate a non-admin user

    with patch('app.database.product_collection.insert_one', new_callable=AsyncMock) as mock_insert_one:
        mock_insert_one.return_value.inserted_id = "mock_product_id"


    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.99,
        "category": "Test Category",
        "inventory_count": 100
    }

    response = client.post("/products/", json=product_data, headers=headers2)

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

def test_get_product_success():
    with patch('app.database.product_collection.find_one', new_callable=AsyncMock) as mock_find_one:
        mock_find_one.return_value = {
            "_id": ObjectId("64b73e51234ab2c73c056bb3"),
            "name": "Test Product",
            "description": "A test product",
            "price": 10.99,
            "category": "Test Category",
            "inventory_count": 100,
            "reviews": [{"rating": 4}, {"rating": 5}]
        }

        response = client.get("/products/64b73e51234ab2c73c056bb3", headers=headers1)
        assert response.status_code == 200
        assert response.json()["average_rating"] == 4.5
        assert response.json()["latest_reviews"] == [{"rating": 4}, {"rating": 5}]

def test_get_product_invalid_id():
    response = client.get("/products/invalid_id", headers=headers2)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid product ID"}

def test_get_product_not_found():
    with patch('app.database.product_collection.find_one', new_callable=AsyncMock) as mock_find_one:
        mock_find_one.return_value = None

        response = client.get("/products/64b73e51234ab2c73c056bb3", headers=headers2)
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}

def test_add_review_success():
    with patch('app.database.product_collection.update_one', new_callable=AsyncMock) as mock_update_one:
        mock_update_one.return_value.modified_count = 1

        review_data = {
            "rating": 5,
            "comment": "Great product!"
        }
        response = client.post(
            "/products/64b73e51234ab2c73c056bb3/reviews",
            json=review_data,
            headers=headers2
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Review added successfully"}

def test_add_review_product_not_found():
    with patch('app.database.product_collection.update_one', new_callable=AsyncMock) as mock_update_one:
        mock_update_one.return_value.modified_count = 0

        review_data = {
            "rating": 5,
            "comment": "Great product!"
        }
        response = client.post(
            "/products/64b73e51234ab2c73c056bb3/reviews",
            json=review_data,
            headers=headers2
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}