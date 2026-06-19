from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    app_name: str = "Azure Code Agent"

    # Azure OpenAI (placeholder for now)
    azure_openai_endpoint: str = ""
    azure_openai_key: str = ""

    # Database (placeholder)
    database_url: str = ""

    class Config:
        env_file = ".env"


settings = Settings()