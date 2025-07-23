import uuid
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Index
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .reviews import Review

class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    year: int = Field(index=True)
    description: str = Field(index=True)
    wishlist: bool = Field(default=False)
    # Number of letters in the movie title
    title_length: int = Field(default=0)
    rating: str = Field(default="NR", max_length=5, description="MPA rating (G, PG, PG-13, R, NC-17, NR)", index=True)

    # Relationship to reviews (one-to-many)
    reviews: List["Review"] = Relationship(back_populates="movie")
 