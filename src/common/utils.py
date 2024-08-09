import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Paths:
    DATA: Path = Path("data")
    ADR = DATA / "adr"
    UKDS = DATA / "ukds"
    CDRC = DATA / "cdrc"

    @classmethod
    def ensure_directories_exist(cls):
        cls.ADR.mkdir(parents=True, exist_ok=True)
        cls.UKDS.mkdir(parents=True, exist_ok=True)
        cls.CDRC.mkdir(parents=True, exist_ok=True)


Paths.ensure_directories_exist()


def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [
                f"Document {i+1}:\n\n{d.page_content}\nMetadata: {d.metadata}"
                for i, d in enumerate(docs)
            ]
        )
    )


def clean_string(text: str) -> str:
    # remove content between /* ... */ (CSS or other style definitions)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    # remove anything within XML or HTML tags
    text = re.sub(r"<.*?>", "", text)
    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # remove line breaks where there's no punctuation before the break
    # match a lowercase letter or a word followed by a newline, and then another lowercase letter
    text = re.sub(r"(\w)(\s*\n\s*)(\w)", r"\1 \3", text)
    return text
