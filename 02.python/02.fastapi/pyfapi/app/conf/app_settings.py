from pydantic_settings import BaseSettings

from app.conf.env.cors_config import CorsSettings
from app.conf.env.db_config import DatabaseSettings
from app.conf.env.email_config import SMTPSettings
from app.conf.env.jwt_config import JWTSettings
from app.conf.env.log_config import LoggingSettings
from app.conf.env.security_settings import SecuritySettings
from app.conf.env.server_config import ServerSettings


class ApplicationSettings(BaseSettings):
    """
    Application settings
    """
    APP_NAME: str = "PyFAPI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more."
    APP_URL: str = "http://localhost:8000"
    APP_DEBUG: bool = True

    # class Config:
    #     # env_prefix = "APP_"
    #     env_file = ".env.dev"
    #     env_file_encoding = "utf-8"
    #     case_sensitive = True
    #     extra = "allow"
    model_config = {
        "env_file": ".env.dev",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow"
    }


app_settings = ApplicationSettings()
log_settings = LoggingSettings()
db_settings = DatabaseSettings()
cors_settings = CorsSettings()
email_settings = SMTPSettings()
server_settings = ServerSettings()
jwt_settings = JWTSettings()
security_settings = SecuritySettings()
