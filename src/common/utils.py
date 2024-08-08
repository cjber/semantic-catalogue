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
