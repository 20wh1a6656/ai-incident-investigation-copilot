import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get absolute path of backend directory and project root directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Incident Investigation Copilot"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # DB configs (Absolute paths relative to the project root)
    SQLITE_DB_PATH: str = os.path.join(PROJECT_ROOT, "data", "incidents.db")
    CHROMA_DB_PATH: str = os.path.join(PROJECT_ROOT, "data", "chroma_db")
    
    # Provider configs
    ACTIVE_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    DEFAULT_MODEL: str = "mock-model"

    # CORS configs
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
