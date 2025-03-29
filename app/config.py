from pydantic import BaseSettings


class Settings(BaseSettings):
    OLLAMA_API_URL: str
    OLLAMA_API_AUTH: str

    class Config:
        env_file = "../.env"


settings = Settings()
