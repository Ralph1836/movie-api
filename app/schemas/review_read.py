from pydantic import BaseModel  # Import Pydantic's BaseModel for schema definition
from typing import Optional  # For optional fields
from datetime import datetime  # For datetime type

class ReviewRead(BaseModel):
    user_name: str  # Name of the reviewer
    gender: str  # Gender of the reviewer
    age: int  # Age of the reviewer
    review_text: str  # The review content
    rating: float  # Numeric rating
    created_at: datetime  # Timestamp of the review

    class Config:
        from_attributes = True  # Enable ORM mode for Pydantic v2 