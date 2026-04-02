# Create the single instance of your connector
from backend.dataLayer.DatabaseConnector import DatabaseConnector

db_connector = DatabaseConnector()


def get_db():
    """FastAPI dependency that uses the Singleton connector."""
    db = db_connector._SessionLocal()  # Access the factory created in _initialize
    try:
        yield db
    finally:
        db.close()
