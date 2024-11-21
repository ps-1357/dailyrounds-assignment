from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ReviewModel(BaseModel):
    rating: int = Field(..., ge=1, le=5)  # Rating must be between 1 and 5
    comment: str

    @field_validator("comment")
    def validate_comment(cls, value):
        if "<script>" in value.lower():
            raise ValueError("Invalid input detected")
        return value

class ProductModel(BaseModel):
    name: str
    category: str
    price: float = Field(..., gt=0)  # Price must be positive
    inventory_count: int
    description: Optional[str] = None
    image_urls: Optional[list] = None