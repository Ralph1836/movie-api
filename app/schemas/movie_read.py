from pydantic import BaseModel  # Import Pydantic's BaseModel for schema definition
from typing import List  # For type hinting lists
import uuid  # For UUID type
from app.schemas.review_read import ReviewRead  # Import the ReviewRead schema for nested reviews

class MovieRead(BaseModel):
    id: uuid.UUID  # Movie ID as UUID
    title: str  # Movie title
    year: int  # Release year
    description: str  # Movie description
    wishlist: bool = False  # Wishlist status
    title_length: int = 0  # Number of letters in the movie title
    rating: str = "NR"  # MPA rating
    reviews: List[ReviewRead] = []  # List of reviews for the movie
    

    class Config:
        from_attributes = True  # Enable ORM mode for Pydantic v2 