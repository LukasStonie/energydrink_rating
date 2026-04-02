import contextlib
import os

from backend.config.ConfigKeys import ConfigKeys, SQLiteConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnector:
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the database engine and session factory."""
        path = os.getenv(ConfigKeys.DB_CONFIG_PATH)
        if not path:
            raise ValueError(
                f"Database configuration path not set. Please set the environment variable {ConfigKeys.DB_CONFIG_PATH}.")
        self._conf = SQLiteConfig(
            config_path=path)
        self._engine = create_engine(
            self._conf.Database_Connection_String,
            echo=False,
            connect_args={
                "check_same_thread": False
            } if "sqlite" in self._conf.Database_Connection_String else {}
        )
        self._SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @contextlib.contextmanager
    def get_db(self):
        """Context manager to get a database session."""
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def init_db(self):
        """Initialize the database schema."""
        print(f"Database initialized at: {self._conf.Database_Folder}")

    @property
    def engine(self):
        return self._engine


# Usage
if __name__ == "__main__":
    connector = DatabaseConnector()
    connector.init_db()
