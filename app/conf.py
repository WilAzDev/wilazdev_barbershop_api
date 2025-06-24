from typing import List
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings,SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    secret_key: str
    app_name: str
    items_per_user: int

    algorithm: str
    access_token_expire_minutes: int
    
    db_engine: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    
    admin_email: str
    
    origins : List[str]
    
    @property
    def db_url(self):
        if self.db_engine == 'postgresql':
            if self.db_password:
                return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            else:
                return f"postgresql+asyncpg://{self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()