from pydantic_settings import BaseSettings
import logging
import sys

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    log_level: str = "INFO"  # 可用 ENV 調整

    class Config:
        env_file = ".env"

settings = Settings()

# 設定全局 logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("fin-iq-api")
logger.info("Logging is configured. Level: %s", settings.log_level)
