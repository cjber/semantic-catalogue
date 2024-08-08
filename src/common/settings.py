import tomllib

from pydantic import Field
from pydantic_settings import BaseSettings

with open("./config/config.toml", "rb") as f:
    Config = tomllib.load(f)


class DataStoreSettings(BaseSettings):
    index_name: str = Field(min_length=1)
    host: str = Field(min_length=1)
    embed_model: str = Field(min_length=1)
    embed_dim: int = Field(gt=0, le=10_000)
    chunk_size: int = Field(gt=0, le=10_000)
    chunk_overlap: int = Field(ge=0, le=10_000)


class ModelSettings(BaseSettings):
    llm: str = Field(min_length=1)
    top_k: int = Field(gt=0, le=100)


class Settings(BaseSettings):
    model: ModelSettings = ModelSettings.model_validate(Config["model"])
    datastore: DataStoreSettings = DataStoreSettings.model_validate(Config["datastore"])


cfg = Settings()
