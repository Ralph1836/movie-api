import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .movies import Movie  # Only import for type checking to avoid circular import

class Review(SQLModel, table=True):
    __tablename__ = "reviews"  # Table name in the database

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # Primary key
    movie_id: uuid.UUID = Field(foreign_key="movies.id", index=True)  # Foreign key to movies
    user_name: str  # Name of the reviewer
    gender: str  # Gender of the reviewer
    age: int  # Age of the reviewer
    review_text: str  # The review content
    rating: float  # Numeric rating
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Timestamp

    # Relationship to the Movie (many-to-one)
    movie:"Movie" = Relationship(back_populates="reviews")