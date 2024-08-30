from pathlib import Path
from typing import Iterator

import dateparser
import polars as pl
from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from src.common.utils import Paths, clean_string


class CDRCLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        if self.file_path.endswith(".pdf"):
            documents = PDFMinerLoader(self.file_path).load()
            metadata = self._add_cdrc_pdf_metadata(self.file_path)

            for d in documents:
                d.page_content = clean_string(d.page_content)
                d.metadata |= metadata | {"file_path": self.file_path}
                yield d
        elif self.file_path.endswith(".txt"):
            with open(self.file_path, encoding="utf-8") as f:
                content = f.read()
                yield Document(
                    page_content=content,
                    metadata={"file_path": self.file_path}
                    | self._add_cdrc_txt_metadata(self.file_path),
                )

    @staticmethod
    def _add_cdrc_txt_metadata(file_path: str) -> dict[str, str]:
        id = Path(file_path).stem.rsplit("-", maxsplit=1)[0]
        cdrc_meta = pl.read_parquet(Paths.CDRC / "cdrc_metadata.parquet")

        metadata = cdrc_meta.filter(pl.col("id") == id)
        iso_date = dateparser.parse(metadata["metadata_created"][0]).isoformat()  # type: ignore
        return {
            "title": metadata["title"][0],
            "id": metadata["id"][0],
            "url": metadata["url"][0],
            "date_created": iso_date,
            "source": "CDRC",
        }

    @staticmethod
    def _add_cdrc_pdf_metadata(file_path: str) -> dict[str, str]:
        id = Path(file_path).stem
        main_id = "-".join(id.split("-")[:5])
        resource_id = "-".join(id.split("-")[5:])

        cdrc_meta = pl.read_parquet(Paths.CDRC / "cdrc_metadata.parquet")
        cdrc_pdf_meta = pl.read_parquet(Paths.CDRC / "cdrc_resource_metadata.parquet")

        resource = cdrc_pdf_meta.filter(pl.col("resource_id") == resource_id)
        metadata = cdrc_meta.filter(pl.col("id") == main_id)

        iso_date = dateparser.parse(resource["created"][0]).isoformat()  # type: ignore
        return {
            "title": metadata["title"][0],
            "id": metadata["id"][0],
            "url": metadata["url"][0],
            "date_created": iso_date,
            "source": "CDRC",
        }


class ADRLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        with open(self.file_path, encoding="utf-8") as f:
            content = f.read()
            yield Document(
                page_content=content,
                metadata={"file_path": self.file_path}
                | self._add_adr_metadata(self.file_path),
            )

    @staticmethod
    def _add_adr_metadata(file_path: str) -> dict[str, str]:
        doc_id, origin_id, _ = Path(file_path).stem.split("-")
        metadata = (
            pl.scan_parquet(Paths.ADR / "adr_datasets.parquet")
            .filter((pl.col("id") == doc_id) & (pl.col("origin_id") == origin_id))
            .collect()[0]
            .to_dict(as_series=False)
        )
        if len(metadata["id"]) == 0:
            return {}

        date_created = metadata["publication_date"][0]
        date_created = (
            dateparser.parse(date_created).isoformat()  # type: ignore
            if isinstance(date_created, str)
            else ""
        )
        return {
            "title": metadata["name"][0],
            "id": f"{doc_id}-{origin_id}",
            "url": metadata["url"][0],
            "date_created": date_created,
            "source": "ADR",
        }


class UKDSLoader(BaseLoader):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        with open(self.file_path, encoding="utf-8") as f:
            content = f.read()
            yield Document(
                page_content=content,
                metadata={"file_path": self.file_path}
                | self._add_ukds_metadata(self.file_path),
            )

    @staticmethod
    def _add_ukds_metadata(file_path: str) -> dict[str, str]:
        doc_id = Path(file_path).stem.split("-")[0]
        metadata = (
            pl.scan_parquet(Paths.UKDS / "ukds.parquet")
            .with_columns(pl.col("url").str.split("=").list[1].alias("id"))
            .filter(pl.col("id") == doc_id)
            .collect()
            .to_dict(as_series=False)
        )
        if len(metadata["id"]) == 0:
            return {}

        date_created = (
            dateparser.parse(metadata["date"][0]).isoformat()  # type: ignore
            if isinstance(metadata["date"][0], str)
            else ""
        )
        return {
            "title": metadata["title"][0],
            "id": doc_id,
            "url": metadata["url"][0],
            "date_created": date_created,
            "source": "UKDS",
        }
