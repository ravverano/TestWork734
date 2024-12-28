from pydantic import (
    BaseSettings,
    validator,
    PostgresDsn
)
from typing import Any, Dict, Optional

class Settings(BaseSettings):
    # POSTGRES
    PSQL_USER: str
    PSQL_PASSWORD: str
    PSQL_HOST: str
    PSQL_PORT: str
    PSQL_DBNAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("PSQL_USER"),
            password=values.get("PSQL_PASSWORD"),
            host=values.get("PSQL_HOST"),
            port=values.get("PSQL_PORT"),
            path=f"/{values.get('PSQL_DBNAME') or ''}",
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

settings = Settings()
