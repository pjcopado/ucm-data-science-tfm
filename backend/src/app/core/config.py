import os
import dotenv
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class Settings(BaseSettings):

    # PROJECT INFO
    TITLE: str = "Chatbot"
    VERSION: str = "0.0.1"
    DESCRIPTION: str | None = None
    DEBUG: bool = True

    # APP SETTINGS
    ROOT_PATH: str = ""
    OPENAPI_URL: str | None = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    API_V1_STR: str = "/v1"
    SWAGGER_ENABLED: bool = True

    RATE_LIMIT_ENABLED: bool = True

    IS_ALLOWED_CREDENTIALS: bool = True
    ALLOWED_ORIGINS: list[str] = ["localhost", "127.0.0.1"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # DATABASE SETTINGS
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "chatbot"

    DB_MIN_POOL_CON: int = 10
    DB_MAX_POOL_CON: int = 80
    DB_POOL_SIZE: int = 100
    DB_POOL_OVERFLOW: int = 20
    DB_TIMEOUT: int = 5
    IS_DB_ECHO_LOG: bool = False
    IS_DB_EXPIRE_ON_COMMIT: bool = False
    IS_DB_FORCE_ROLLBACK: bool = False

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """

        if not self.SWAGGER_ENABLED:
            self.OPENAPI_URL = None

        return {
            "title": self.TITLE,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "root_path": self.ROOT_PATH,
            "contact": {
                "name": "backend team",
                "url": "https://www.chatbot.io",
                "email": "backend@chatbot.com",
            },
            "swagger_ui_parameters": {
                "defaultModelsExpandDepth": -1,
                "defaultModelExpandDepth": 10,
            },
        }


class LocalSettings(Settings):

    model_config = SettingsConfigDict(
        env_file=f"{str(ROOT_DIR)}/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_assignment=True,
        extra="allow",
    )


class DockerSettings(Settings):

    model_config = SettingsConfigDict(
        env_file=f"{str(ROOT_DIR)}/.env.docker",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_assignment=True,
        extra="allow",
    )


ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "local":
    settings = LocalSettings()

settings = DockerSettings() if ENVIRONMENT == "DOCKER" else LocalSettings()
