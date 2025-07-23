from sqlmodel import create_engine, Session

# Define the SQLite database URL
sqlite_url = "sqlite:///database.db"
# Create the database engine (echo=True prints SQL statements for debugging)
engine = create_engine(sqlite_url, echo=True)

# Dependency function for FastAPI to provide a database session
# Ensures the session is closed after use
def get_session():
    with Session(engine) as session:
        yield session 