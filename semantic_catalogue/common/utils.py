import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()


class Paths:
    """
    Manage and ensure the existence of directory paths used in the project.

    Attributes
    ----------
    DATA : Path
        Base path for data storage.
    ADR : Path
        Path for ADR data.
    UKDS : Path
        Path for UKDS data.
    CDRC : Path
        Path for CDRC data.
    CONFIG : Path
        Path for configuration files.
    """

    DATA: Path = Path("data")
    ADR = DATA / "adr"
    UKDS = DATA / "ukds"
    CDRC = DATA / "cdrc"

    CONFIG = Path("config")

    @classmethod
    def ensure_directories_exist(cls):
        cls.ADR.mkdir(parents=True, exist_ok=True)
        cls.UKDS.mkdir(parents=True, exist_ok=True)
        cls.CDRC.mkdir(parents=True, exist_ok=True)


Paths.ensure_directories_exist()


def clean_string(text: str) -> str:
    """
    Clean a string by removing comments, HTML tags, and extra whitespace.

    :param text: The text to be cleaned.
    :type text: str
    :return: The cleaned text.
    :rtype: str
    """
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", " <PARAGRAPH_BREAK> ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = text.replace(" <PARAGRAPH_BREAK> ", "\n\n")
    text = text.strip()
    return text


def format_docs_with_id(docs: list[Document]) -> str:
    """
    Format a list of documents with their source IDs for display.

    :param docs: A list of Document objects to be formatted.
    :type docs: list of Document
    :return: A formatted string representation of the documents with their source IDs.
    :rtype: str
    """
    formatted = [
        f"Source ID: {i}\nArticle Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
        for i, doc in enumerate(docs)
    ]
    return "\n\n" + "\n\n".join(formatted)
