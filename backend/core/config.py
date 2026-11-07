# será responsável por ler os dados do textuais do env e tornar em objetos utilziaveis pelo python

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    groq_api_key: str
    jwt_secret_key: str
    database_url :str = "sqlite///./treino.db"

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()