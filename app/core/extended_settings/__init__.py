from .app_settings import AppSettings
from .database_settings import DatabaseSettings
from .llm_settings import LLMSettings
from .logger_settings import LoggerSettings

# Instantiate and export commonly used settings objects.
# This lets other modules do: from app.core.extended_settings import app_settings
app_settings = AppSettings()
db_settings = DatabaseSettings()
llm_settings = LLMSettings()
logger_settings = LoggerSettings()

__all__ = [
    "app_settings",
    "db_settings",
    "llm_settings",
    "logger_settings",
    "AppSettings",
    "DatabaseSettings",
    "LLMSettings",
    "LoggerSettings",
]
