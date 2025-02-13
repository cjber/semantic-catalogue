import tomllib

from pydantic import Field
from pydantic_settings import BaseSettings

from semantic_catalogue.common.utils import Paths

with open(Paths.CONFIG / "config.toml", "rb") as f:
    Config = tomllib.load(f)


class DataStoreSettings(BaseSettings):
    """
    DataStoreSettings holds configuration for the data store.

    :ivar index_name: The name of the index. Must have a minimum length of 1.
    :vartype index_name: str
    :ivar host: The host address. Must have a minimum length of 1.
    :vartype host: str
    :ivar embed_model: The embedding model name. Must have a minimum length of 1.
    :vartype embed_model: str
    :ivar embed_dim: The dimension of the embedding. Must be greater than 0 and less than or equal to 10,000.
    :vartype embed_dim: int
    :ivar chunk_size: The size of the data chunks. Must be greater than 0 and less than or equal to 10,000.
    :vartype chunk_size: int
    :ivar chunk_overlap: The overlap size of the data chunks. Must be greater than or equal to 0 and less than or equal to 10,000.
    :vartype chunk_overlap: int
    """

    index_name: str = Field(min_length=1)
    host: str = Field(min_length=1)
    embed_model: str = Field(min_length=1)
    embed_dim: int = Field(gt=0, le=10_000)
    chunk_size: int = Field(gt=0, le=10_000)
    chunk_overlap: int = Field(ge=0, le=10_000)


class ModelSettings(BaseSettings):
    """
    ModelSettings holds configuration for the model.

    :ivar llm: The language model name. Must have a minimum length of 1.
    :vartype llm: str
    :ivar top_k: The top K results to consider. Must be greater than 0 and less than or equal to 15,000.
    :vartype top_k: int
    :ivar alpha: The alpha parameter. Must be between 0.0 and 1.0 inclusive.
    :vartype alpha: float
    :ivar max_iterations: The maximum number of iterations. Must be greater than 0 and less than 10.
    :vartype max_iterations: int
    """

    llm: str = Field(min_length=1)
    top_k: int = Field(gt=0, le=15_000)
    alpha: float = Field(ge=0.0, le=1.0)
    max_iterations: int = Field(gt=0, lt=10)


class Settings(BaseSettings):
    """
    Settings aggregates all configuration settings.

    :ivar model: The model settings.
    :vartype model: ModelSettings
    :ivar datastore: The data store settings.
    :vartype datastore: DataStoreSettings
    """

    model: ModelSettings = ModelSettings.model_validate(Config["model"])
    datastore: DataStoreSettings = DataStoreSettings.model_validate(Config["datastore"])


cfg = Settings()
