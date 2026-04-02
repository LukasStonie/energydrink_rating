import json


class ConfigKeys:
    """Config keys for the application."""
    # Database configuration
    DB_CONFIG_PATH = "DB_CONFIG_PATH"


class SQLiteConfig:
    """Config keys for the application."""
    # Database configuration
    Database_Folder: str
    Database_File_Name: str
    Database_Connection_String: str

    def __init__(self, config_path: str = None):
        """Initialize the configuration."""
        if config_path:
            self.load_from_file(config_path)
            self.Database_Connection_String = f"sqlite:///{self.Database_Folder}/{self.Database_File_Name}"
        else:
            raise ValueError(
                "Config path must be provided to load configuration.")

    def __str__(self):
        return f"SQLiteConfig(Database_Folder={self.Database_Folder}, Database_File_Name={self.Database_File_Name})"

    def load_from_file(self, file_path: str):
        """Load configuration from a file."""
        # Implement logic to read from a file and populate the fields
        with open(file_path, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                setattr(self, key, value)


if __name__ == "__main__":
    conf = SQLiteConfig(
        config_path="/workspaces/energydrink_rating/energy_drink_rating/database_config.json")
    print(conf)
