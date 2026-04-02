# Create the single instance of your connector
from backend.dataLayer.DatabaseConnector import DatabaseConnector

db_connector = DatabaseConnector()


def get_db():
    """FastAPI dependency that uses the Singleton connector."""
    # Delegate session lifecycle management to the connector's public API
    with db_connector.get_db() as db:
        yield db
