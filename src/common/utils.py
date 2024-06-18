from pathlib import Path


class Paths:
    DATA = Path("data")
    ADR = DATA / "adr"


class Consts:
    INDEX_NAME = "data-catalogue"
    EMBEDDING_MODEL = "text-embedding-3-large"
    EMBEDDING_DIM = 3072
