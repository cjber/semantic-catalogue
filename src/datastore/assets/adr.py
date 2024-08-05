import itertools
import json

import polars as pl
import requests
from dagster import AssetExecutionContext, asset
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from src.common.utils import Paths

PAGE_SIZE = 100
API_VERSION = "2.0"
BASE_URL = "https://api-datacatalogue.adruk.org/api"


@asset
def adr_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"X-API-Version": API_VERSION})
    return session


@asset
def adr_datasets_id(
    context: AssetExecutionContext, adr_session: requests.Session
) -> pl.DataFrame:
    datasets = []
    for page_number in itertools.count(start=1):
        context.log.info(f"Fetching page {page_number}")
        datasets_page = _fetch_datasets_page(context, adr_session, page_number)
        if "end" in datasets_page:
            context.log.info(f"End of pages reached at {datasets_page['end']}")
            break
        datasets.extend(datasets_page)
    df = (
        pl.DataFrame(datasets)
        .select(["origin", "id", "searchResultType", "title"])
        .filter(pl.col("searchResultType") == "PHYSICAL")
        .with_columns(pl.col("origin").struct[0].alias("origin_id"))
    )
    df.write_parquet(Paths.ADR / "adr_datasets_id.parquet")

    return df


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _fetch_datasets_page(
    context: AssetExecutionContext, adr_session: requests.Session, page_number: int
) -> dict:
    params = {
        "pageSize": PAGE_SIZE,
        "pageNumber": page_number,
        "include": "dataset::dataelement::dataclass",
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string",
        "state": "START",
    }
    try:
        response = adr_session.get(f"{BASE_URL}/{{sql}}/dataset", params=params)
        response.raise_for_status()
        content = json.loads(response.content)["content"]
        if not content:
            return {"end": page_number}
        return content
    except requests.HTTPError as http_err:
        context.log.error(f"HTTP error occurred: {http_err}")
        return {}
    except Exception as err:
        context.log.error(f"Other error occurred: {err}")
        return {}


@asset
def adr_datasets(
    context: AssetExecutionContext,
    adr_session: requests.Session,
    adr_datasets_id: pl.DataFrame,
) -> pl.DataFrame:

    datasets_list = []
    for row in tqdm(adr_datasets_id.rows(named=True), total=len(adr_datasets_id)):
        dataset = _fetch_dataset_info(context, adr_session, row)
        if dataset:
            datasets_list.append(dataset)
    df = pl.json_normalize(datasets_list)
    df.write_parquet(Paths.ADR / "adr_datasets.parquet")

    return df


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _fetch_dataset_info(
    context: AssetExecutionContext, adr_session: requests.Session, row: dict
) -> dict:
    url = f"{BASE_URL}/dataset/{row['id']}?originId={row['origin_id']}"
    try:
        response = adr_session.get(url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        context.log.error(f"HTTP error occurred: {http_err}")
        return {}
    except Exception as err:
        context.log.error(f"Other error occurred: {err}")
        return {}
    content = json.loads(response.content)

    return {
        "id": row["id"],
        "name": row["title"],
        "origin_name": content["origin"]["name"],
        "origin_id": row["origin_id"],
        "doi": content["summary"].get("doiName"),
        "url": content["origin"]["link"],
        "keywords": content["summary"].get("keywords"),
        "abstract": content["summary"]["abstract"],
        "description": content.get("documentation", {}).get("description"),
        "publication_date": content["summary"].get("publicationDate"),
    }


@asset
def adr_descriptions(adr_datasets: pl.DataFrame) -> None:
    outdir = Paths.ADR / "txt"
    outdir.mkdir(parents=True, exist_ok=True)

    for item in adr_datasets.rows(named=True):
        with open(
            outdir / f"{item['id']}-{item['origin_id']}-description.txt",
            "w",
        ) as f:
            f.write(
                f"Dataset Title: {item['name']}"
                f"\n\nDescription: \n\n{item['description']}"
                f"\n\nAbstract: \n\n{item['abstract']}"
            )
