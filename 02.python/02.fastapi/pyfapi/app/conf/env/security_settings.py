from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    # TODO security.enabled not implemented yet
    ENABLED: bool = False
    # List of paths that do not require authorization like /docs,/redoc,/openapi.json,/health,/ping,/,/api/v1,/api/v1/public,/api/v1/auth/login,/api/v1/auth/register
    
    # Q. http://localhost:8000/api/v1/docs 같은 사이트 접속 안되면?
    # A. .env.dev에 SECURITY_ALLOWED_PATHS 가 아래 ALLOWED_PATH 에 안들어간거니까, 수동으로 써라.
    # ALLOWED_PATHS: list[str] = ["/favicon.ico","/docs","/api/v1/docs","/api/v1/redoc","/redoc","/api/v1/openapi.json","/openapi.json","/api/v1/health","/health","/ping","/","/api/v1","/api/v1/public","/api/v1/auth/login","/api/v1/auth/register"]
    ALLOWED_PATHS: list[str] = []

    # class Config:
    #     env_prefix = "SECURITY_"
    #     env_file = ".env.dev"
    #     env_file_encoding = "utf-8"
    #     case_sensitive = True

    model_config = {
        "env_prefix": "SECURITY_",
        "env_file": ".env.dev",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow"  # 추가 필드 허용
    }
