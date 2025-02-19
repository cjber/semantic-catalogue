from pathlib import Path
from typing import Iterator

import dateparser
import polars as pl
from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from semantic_catalogue.common.utils import Paths, clean_string


class CDRCLoader(BaseLoader):
    """
    Loader for CDRC documents.

    :param file_path: Path to the file to be loaded.
    :type file_path: str
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the CDRCLoader.

        :param file_path: Path to the file to be loaded.
        :type file_path: str
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily load documents from the file.

        Processes both PDFs and txt files.

        :yield: Document objects with content and metadata.
        :rtype: Iterator[Document]
        """
        if self.file_path.endswith(".pdf"):
            try:
                documents = PDFMinerLoader(self.file_path).load()
            except Exception as e:
                print(f"PDF file not read: {e}")
                documents = [Document(page_content="")]

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
        """
        Add metadata for CDRC text files.

        :param file_path: Path to the text file.
        :type file_path: str
        :return: Metadata dictionary.
        :rtype: dict[str, str]
        """
        id = Path(file_path).stem.rsplit("-", maxsplit=1)[0]
        cdrc_meta = pl.read_parquet(Paths.CDRC / "cdrc_metadata.parquet")

        metadata = cdrc_meta.filter(pl.col("id") == id)
        iso_date = dateparser.parse(metadata["metadata_created"][0]).isoformat()
        return {
            "title": metadata["title"][0],
            "id": metadata["id"][0],
            "url": metadata["url"][0],
            "date_created": iso_date,
            "source": "CDRC",
        }

    @staticmethod
    def _add_cdrc_pdf_metadata(file_path: str) -> dict[str, str]:
        """
        Add metadata for CDRC PDF files.

        :param file_path: Path to the PDF file.
        :type file_path: str
        :return: Metadata dictionary.
        :rtype: dict[str, str]
        """
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
    """
    Loader for ADR documents.

    :param file_path: Path to the file to be loaded.
    :type file_path: str
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the ADRLoader.

        :param file_path: Path to the file to be loaded.
        :type file_path: str
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily load documents from the file.

        :yield: Document objects with content and metadata.
        :rtype: Iterator[Document]
        """
        with open(self.file_path, encoding="utf-8") as f:
            content = f.read()
            yield Document(
                page_content=content,
                metadata={"file_path": self.file_path}
                | self._add_adr_metadata(self.file_path),
            )

    @staticmethod
    def _add_adr_metadata(file_path: str) -> dict[str, str]:
        """
        Add metadata for ADR files.

        :param file_path: Path to the file.
        :type file_path: str
        :return: Metadata dictionary.
        :rtype: dict[str, str]
        """
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
    """
    Loader for UKDS documents.

    :param file_path: Path to the file to be loaded.
    :type file_path: str
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the UKDSLoader.

        :param file_path: Path to the file to be loaded.
        :type file_path: str
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily load documents from the file.

        :yield: Document objects with content and metadata.
        :rtype: Iterator[Document]
        """
        with open(self.file_path, encoding="utf-8") as f:
            content = f.read()
            yield Document(
                page_content=content,
                metadata={"file_path": self.file_path}
                | self._add_ukds_metadata(self.file_path),
            )

    @staticmethod
    def _add_ukds_metadata(file_path: str) -> dict[str, str]:
        """
        Add metadata for UKDS files.

        :param file_path: Path to the file.
        :type file_path: str
        :return: Metadata dictionary.
        :rtype: dict[str, str]
        """
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
            dateparser.parse(metadata["date"][0]).isoformat()
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
