from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    bot_token: str = Field(..., alias="BOT_TOKEN")
    telegraph_access_token: str = Field(..., alias="TELEGRAPH_ACCESS_TOKEN")
    default_author_name: str = Field("MD Telegraph Bot", alias="DEFAULT_AUTHOR_NAME")
    default_author_url: HttpUrl | None = Field(None, alias="DEFAULT_AUTHOR_URL")
    max_md_size: int = Field(30000, alias="MAX_MD_SIZE")
    max_pages_per_request: int = Field(5, alias="MAX_PAGES_PER_REQUEST")
    user_rate_limit_per_minute: int = Field(6, alias="USER_RATE_LIMIT_PER_MINUTE")
    enable_personal_accounts: bool = Field(False, alias="ENABLE_PERSONAL_ACCOUNTS")
    accounts_db_path: str = Field("data/accounts.db", alias="ACCOUNTS_DB_PATH")
    default_locale: str = Field("en", alias="DEFAULT_LOCALE")
    locales_dir: str = Field("app/locales", alias="LOCALES_DIR")
    log_level: str = Field("INFO", alias="LOG_LEVEL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

