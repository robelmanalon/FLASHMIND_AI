from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    app_env: str = "development"
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_role_key: str = ""
    supabase_auto_confirm_users: bool = False
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    database_url: str = ""
    frontend_url: str = "http://localhost:5173"

    # Resolve backend/.env from this file so Uvicorn can be launched from any directory.
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()