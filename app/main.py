from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from app.models.movies import Movie
from app.schemas.movie_read import MovieRead
from app.db import get_session
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from aws_lambda_powertools import Logger

app = FastAPI()

#Lambda handler
logger = Logger()
handler = Mangum(app)
handler = logger.inject_lambda_context(handler, clear_state=True)

def lambda_handler(event, context):
    logger.info(f"Lambda event: {event}")
    response = handler(event, context)
    logger.info(f"Lambda response: {response}")
    return response

# Allow access from any origin (n8n needs this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to get all movies with their reviews
@app.get("/movies/", response_model=list[MovieRead])
def get_all_movies_with_reviews(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()  # Query all movies
    return movies

# Endpoint to search movies by partial name (case-insensitive)
@app.get("/movies/search/", response_model=list[MovieRead])
def search_movies(
    q: str = Query(..., min_length=1, description="Partial movie name"),
    session: Session = Depends(get_session)
):
    movies = session.exec(
        select(Movie).where(Movie.title.ilike(f"%{q}%"))  # Case-insensitive search
    ).all()
    return movies 
