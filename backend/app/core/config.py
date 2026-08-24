from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""
    ai_provider: str = "ollama"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "phi3:mini"
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
