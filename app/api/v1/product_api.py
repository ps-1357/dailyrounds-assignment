from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from bson.objectid import ObjectId

from app.models.product_collection import ProductModel, ReviewModel
from app.database import product_collection
from app.middleware.security_middleware import sanitize_input
from app.dependencies import require_role

router = APIRouter()

def convert_object_ids(obj):
    if isinstance(obj, dict):
        return {k: convert_object_ids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_object_ids(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def product_helper(product):
    """Recursively convert ObjectId instances in the product document to strings."""
    return convert_object_ids(product)

def calculate_average_rating(reviews):
    if not reviews:
        return 0
    total_rating = sum(review.get("rating", 0) for review in reviews)

    return round(total_rating / len(reviews), 2)

@router.post("/")
async def create_product(product: ProductModel, user:dict = Depends(require_role("admin"))):
    product_data = product.model_dump()
    product_data["reviews"] = []
    new_product = await product_collection.insert_one(product_data)
    return {"message": "Product created", "product_id": str(new_product.inserted_id)}


@router.get("/")
async def list_products(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
):
    """Retrieve a list of products with average ratings, pagination, and category filtering."""
    query = {}
    if category:
        query["category"] = category

    skip = (page - 1) * limit
    products = await product_collection.find(query).skip(skip).limit(limit).to_list(length=limit)

    # Convert ObjectId and calculate average ratings
    for product in products:
        product["average_rating"] = calculate_average_rating(product.get("reviews", []))
        product = product_helper(product)

    return products


@router.get("/{product_id}")
async def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["average_rating"] = calculate_average_rating(product.get("reviews", []))
    product["latest_reviews"] = product.get("reviews", [])[:5]
    product = product_helper(product)
    return product


@router.post("/{product_id}/reviews")
async def add_review(product_id: str, review: ReviewModel, request: Request, user: dict = Depends(require_role("customer"))):
    user = request.state.user
    sanitized_comment = sanitize_input(review.comment)
    review_data = {"rating": review.rating, "comment": sanitized_comment, "user_id": user["user_id"]}
    result = await product_collection.update_one({"_id": ObjectId(product_id)}, {"$push": {"reviews": review_data}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Review added successfully"}

@router.get("/{product_id}/reviews")
async def get_reviews(product_id: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    """
    Retrieve reviews for a specific product with pagination.
    """
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Find the product by ID
    product = await product_collection.find_one({"_id": ObjectId(product_id)}, {"reviews": 1})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Extract and paginate reviews
    reviews = product.get("reviews", [])
    start = (page - 1) * limit
    end = start + limit
    paginated_reviews = reviews[start:end]
    
    return {
        "total_reviews": len(reviews),
        "page": page,
        "limit": limit,
        "reviews": paginated_reviews,
    }
