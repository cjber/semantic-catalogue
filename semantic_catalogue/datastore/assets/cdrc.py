import itertools
import os

import polars as pl
import requests
from dagster import AssetExecutionContext, asset
from dotenv import load_dotenv
from tqdm import tqdm

from semantic_catalogue.common.utils import Paths, clean_string

load_dotenv()

METADATA_URL = (
    "https://data.cdrc.ac.uk/api/3/action/current_package_list_with_resources"
)
LOGIN_URL = "https://data.cdrc.ac.uk/user/login"


@asset
def cdrc_metadata(context: AssetExecutionContext) -> list[dict]:
    """
    Fetches metadata from the CDRC API.

    :param context: The execution context provided by Dagster.
    :type context: AssetExecutionContext
    :return: A list of dictionaries containing the metadata.
    :rtype: list[dict]
    :raises requests.HTTPError: If an HTTP error occurs during the request.
    :raises Exception: If any other error occurs during the request.
    """
    try:
        r = requests.get(METADATA_URL)
        r.raise_for_status()
    except requests.HTTPError as http_err:
        context.log.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        context.log.error(f"Other error occurred: {err}")
        raise
    return r.json()["result"][0]


@asset
def cdrc_notes(cdrc_metadata: list[dict]):
    """
    Processes and saves CDRC notes to text files.

    :param cdrc_metadata: A list of dictionaries containing the metadata.
    :type cdrc_metadata: list[dict]
    """
    outdir = Paths.CDRC / "txt"
    outdir.mkdir(parents=True, exist_ok=True)
    for file in outdir.glob("*.txt"):
        file.unlink()

    df = pl.DataFrame(cdrc_metadata).drop(["resources", "tags", "extras"])
    df.write_parquet(Paths.CDRC / "cdrc_metadata.parquet")

    for item in df.rows(named=True):
        with open(Paths.CDRC / "txt" / f"{item['id']}-notes.txt", "w") as f:
            f.write(clean_string(item["notes"]))


@asset
def cdrc_resources(cdrc_metadata: list[dict]) -> pl.DataFrame:
    """
    Processes and saves CDRC resources metadata to a parquet file.

    :param cdrc_metadata: A list of dictionaries containing the metadata.
    :type cdrc_metadata: list[dict]
    :return: A DataFrame containing the resources metadata.
    :rtype: pl.DataFrame
    """
    resources = list(
        itertools.chain.from_iterable(
            [item["resources"] if "resources" in item else [] for item in cdrc_metadata]
        )
    )
    df = pl.concat(
        [
            pl.DataFrame(cdrc_metadata).explode("resources").drop("resources"),
            pl.DataFrame(resources)
            .rename(
                {"id": "resource_id", "url": "resource_url", "name": "resource_name"},
            )
            .drop(["state", "revision_timestamp"]),
        ],
        how="horizontal",
    ).filter((pl.col("format") == "pdf") & (pl.col("resource_url") != ""))
    df.write_parquet(Paths.CDRC / "cdrc_resource_metadata.parquet")
    return df


@asset
def cdrc_session() -> requests.Session:
    """
    Creates and returns a logged-in session for the CDRC API.

    :return: A logged-in session.
    :rtype: requests.Session
    """
    session = requests.Session()
    session.post(
        LOGIN_URL,
        data={
            "name": os.getenv("CDRC_USERNAME"),
            "pass": os.getenv("CDRC_PASSWORD"),
            "form_build_id": os.getenv("CDRC_FORM_BUILD_ID"),
            "form_id": "user_login",
            "op": "Log in",
        },
    )
    return session


@asset
def cdrc_pdfs(
    context: AssetExecutionContext,
    cdrc_session: requests.Session,
    cdrc_resources: pl.DataFrame,
):
    """
    Downloads and saves CDRC PDFs.

    :param context: The execution context provided by Dagster.
    :type context: AssetExecutionContext
    :param cdrc_session: A logged-in session for the CDRC API.
    :type cdrc_session: requests.Session
    :param cdrc_resources: A DataFrame containing the resources metadata.
    :type cdrc_resources: pl.DataFrame
    """
    outdir = Paths.CDRC / "pdf"
    outdir.mkdir(parents=True, exist_ok=True)
    for file in outdir.glob("*.pdf"):
        file.unlink()

    for item in tqdm(cdrc_resources.rows(named=True)):
        context.log.info(f"Processing {item['resource_url']}...")
        filepath = outdir / f"{item['id']}-{item['resource_id']}.pdf"
        try:
            file = cdrc_session.get(item["resource_url"])
            file.raise_for_status()
        except requests.HTTPError as http_err:
            context.log.error(f"HTTP error occurred: {http_err}")
            continue
        except Exception as err:
            context.log.error(f"Other error occurred: {err}")
            continue
        with open(filepath, "wb") as f:
            f.write(file.content)
