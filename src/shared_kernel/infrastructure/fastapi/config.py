from typing import ClassVar
from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DRIVER: ClassVar[str] = "postgresql+psycopg2"
    USER: ClassVar[str] = "mi_usuario"
    PASSWORD: ClassVar[str] = "mi_contraseña"
    HOST: ClassVar[str] = "localhost"
    PORT: ClassVar[str] = "5432"
    DATABASE: ClassVar[str] = "mi_base_de_datos"

    @classmethod
    def get_connection_url(cls):
        return f"{cls.DRIVER}://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"

settings = DatabaseConfig()