import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "database.env")

load_dotenv()
load_dotenv(dotenv_path)


@dataclass
class BaseDBSettings:
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class TestDBSettings(BaseDBSettings):
    DB_HOST: str = os.environ.get("DB_HOST_TEST")
    DB_PORT: str = os.environ.get("DB_PORT_TEST")
    DB_NAME: str = os.environ.get("DB_NAME_TEST")
    DB_USER: str = os.environ.get("DB_USER_TEST")
    DB_PASS: str = os.environ.get("DB_PASS_TEST")


@dataclass
class ProdDBSettings:
    DB_HOST: str = os.environ.get("POSTGRES_HOST")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASS: str = os.environ.get("POSTGRES_PASSWORD")


@dataclass
class FileStorageSettings:
    BASE_DIR: str =  field(init=False, repr=False)
    MEDIA_DIR: str = field(init=False, repr=False)
    MEDIA_URL: str = "/media/"

    def __post_init__(self):
        self.BASE_DIR: str =  os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.MEDIA_DIR: str = os.path.join(self.BASE_DIR, "var\media")
        self.create_media_dir()

    def create_media_dir(self):
        os.makedirs(self.MEDIA_DIR, exist_ok=True)


def get_database_settings():
    env = os.getenv("ENVIRONMENT", "Not database").lower()
    if env == "testing":
        return TestDBSettings()
    elif env == "production":
        return ProdDBSettings()
    else:
        raise ValueError(f"Unknown environment: {env}")


def get_storage_settings():
    settings = FileStorageSettings()
    settings.create_media_dir()
    return settings


database_settings = get_database_settings()
file_storage_settings = get_storage_settings()
