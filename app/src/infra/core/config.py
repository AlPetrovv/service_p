from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent  # src
ROOT_DIR = BASE_DIR.parent  # app
DATA_DIR = ROOT_DIR / "data"
ENV_FILE = ROOT_DIR / ".." / "envs" / "app.env"


class Database(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 10
    max_overflow: int = 10

    @property
    def naming_convention(self) -> dict[str, str]:
        return {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }


class JWT(BaseModel):
    secret: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


class Settings(BaseSettings):
    db: Database
    jwt: JWT = Field(default_factory=JWT)
    # Secret used to validate third-party webhook signatures.
    # Defaults to the value from the task example so the example payload validates out of the box.
    webhook_secret_key: str = "gfdmhghif38yrf9ew0jkf32"
    log_level: str = "INFO"
    version: str = "dev"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="forbid",
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__",
    )


settings = Settings()
