import os
from sqlmodel import create_engine, Session

# Get the DATABASE_URL from environment or fallback to SQLite
database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Create the engine (echo=True prints SQL statements for debugging)
engine = create_engine(database_url, echo=True)

# Dependency function for FastAPI to provide a database session
# Ensures the session is closed after use
def get_session():
    with Session(engine) as session:
        yield session
