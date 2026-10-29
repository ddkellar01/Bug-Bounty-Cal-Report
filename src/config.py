import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "bug-bounty-cal-report"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    monad_rpc_url: str = os.getenv("MONAD_RPC_URL", "https://rpc.monad.xyz")
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
