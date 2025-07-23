from sqlmodel import Session, select  # Import SQLModel session and select for queries
from db import engine  # Import the database engine
from models.movies import Movie  # Import the Movie model
from models.reviews import Review  # Import the Review model
import uuid  # For generating unique IDs
from datetime import datetime, timezone  # For timestamps
from sqlmodel import SQLModel  # For table creation


def seed():
    # List of movies to add
    movies_data = [
        {"title": "Inception", "year": 2010, "description": "A mind-bending thriller.", "wishlist": True, "rating": "PG-13"},
        {"title": "The Matrix", "year": 1999, "description": "A hacker discovers reality is a simulation.", "wishlist": False, "rating": "R"},
        {"title": "Interstellar", "year": 2014, "description": "A journey through space and time.", "wishlist": False, "rating": "PG-13"},
        {"title": "The Godfather", "year": 1972, "description": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.", "wishlist": True, "rating": "R"},
        {"title": "Pulp Fiction", "year": 1994, "description": "The lives of two mob hitmen, a boxer, and others intertwine in four tales of violence and redemption.", "wishlist": True, "rating": "R"},
        {"title": "The Shawshank Redemption", "year": 1994, "description": "Two imprisoned men bond over a number of years.", "wishlist": True, "rating": "R"},
        {"title": "Forrest Gump", "year": 1994, "description": "The presidencies of Kennedy and Johnson, the Vietnam War, and more through the eyes of Forrest.", "wishlist": False, "rating": "PG-13"},
        {"title": "Fight Club", "year": 1999, "description": "An insomniac office worker and a soap maker form an underground fight club.", "wishlist": True, "rating": "R"},
        {"title": "The Dark Knight", "year": 2008, "description": "Batman faces the Joker, a criminal mastermind.", "wishlist": False, "rating": "PG-13"},
        {"title": "Parasite", "year": 2019, "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy and the destitute.", "wishlist": True, "rating": "R"}
    ]

    # List of reviews to add
    reviews_data = [
        {"movie_title": "Inception", "user_name": "Alice", "gender": "F", "age": 30, "review_text": "Amazing visuals and story!", "rating": 9.0},
        {"movie_title": "Inception", "user_name": "Bob", "gender": "M", "age": 25, "review_text": "A bit confusing but great.", "rating": 8.5},
        {"movie_title": "The Matrix", "user_name": "Charlie", "gender": "M", "age": 35, "review_text": "Changed my view of reality!", "rating": 9.5},
        {"movie_title": "The Godfather", "user_name": "Diana", "gender": "F", "age": 40, "review_text": "A masterpiece.", "rating": 10.0},
        {"movie_title": "Pulp Fiction", "user_name": "Eve", "gender": "F", "age": 28, "review_text": "Wild and stylish.", "rating": 9.0},
        {"movie_title": "The Shawshank Redemption", "user_name": "Frank", "gender": "M", "age": 50, "review_text": "Inspiring and emotional.", "rating": 10.0},
        {"movie_title": "Forrest Gump", "user_name": "Grace", "gender": "F", "age": 33, "review_text": "Heartwarming and funny.", "rating": 9.5},
        {"movie_title": "Fight Club", "user_name": "Henry", "gender": "M", "age": 29, "review_text": "Mind-blowing twist!", "rating": 9.0},
        {"movie_title": "The Dark Knight", "user_name": "Ivy", "gender": "F", "age": 27, "review_text": "Best Joker ever.", "rating": 9.5},
        {"movie_title": "Parasite", "user_name": "Jack", "gender": "M", "age": 31, "review_text": "Brilliant social commentary.", "rating": 9.0},
    ]

    with Session(engine) as session:
        # Add movies if not already present
        movie_objs = {}
        for m in movies_data:
            existing = session.exec(select(Movie).where(Movie.title == m["title"]).where(Movie.year == m["year"]).limit(1)).first()
            if existing:
                # Update wishlist if needed
                if existing.wishlist != m.get("wishlist", False):
                    existing.wishlist = m.get("wishlist", False)
                    session.add(existing)
                    session.commit()
                # Update title_length if needed (without changing other columns)
                calculated_length = len(m["title"])
                if existing.title_length != calculated_length:
                    existing.title_length = calculated_length
                    session.add(existing)
                    session.commit()
                # Update rating if needed
                if hasattr(existing, "rating") and existing.rating != m.get("rating", "NR"):
                    existing.rating = m.get("rating", "NR")
                    session.add(existing)
                    session.commit()
                movie_objs[m["title"]] = existing
                continue
            movie = Movie(
                id=uuid.uuid4(),
                title=m["title"],
                year=m["year"],
                description=m["description"],
                wishlist=m.get("wishlist", False),
                # Set title_length for new movies
                title_length=len(m["title"]),
                # Set rating for new movies
                rating=m.get("rating", "NR")
            )
            session.add(movie)
            session.commit()
            session.refresh(movie)
            movie_objs[m["title"]] = movie

        # Add reviews if not already present
        for r in reviews_data:
            movie = movie_objs.get(r["movie_title"])
            if not movie:
                continue
            # Check for duplicate review by user for the same movie
            existing_review = session.exec(
                select(Review).where(Review.movie_id == movie.id).where(Review.user_name == r["user_name"]).limit(1)
            ).first()
            if existing_review:
                continue
            review = Review(
                id=uuid.uuid4(),
                movie_id=movie.id,
                user_name=r["user_name"],
                gender=r["gender"],
                age=r["age"],
                review_text=r["review_text"],
                rating=r["rating"],
                created_at=datetime.now(timezone.utc)
            )
            session.add(review)
        session.commit()

if __name__ == "__main__":
    seed() 