import re
import xml.etree.ElementTree as ET

import polars as pl
import requests
from dagster import AssetExecutionContext, asset
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from semantic_catalogue.common.utils import Paths, clean_string

BASE_URL = "https://oai.ukdataservice.ac.uk:8443/oai/provider"
PARAMS = {"verb": "ListIdentifiers", "metadataPrefix": "ddi", "set": "DataCollections"}
NAMESPACES = {"oai": "http://www.openarchives.org/OAI/2.0/", "ns2": "ddi:codebook:2_5"}


@asset
def ukds_identifiers() -> list[str]:
    """
    Fetches a list of identifiers from the UK Data Service.

    Returns:
        list[str]: A list of identifiers.
    """
    params = PARAMS.copy()

    identifiers = []
    while True:
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

        root = ET.fromstring(response.content)

        headers = root.findall(".//oai:header", NAMESPACES)
        for header in headers:
            if header.attrib.get("status") != "deleted":
                identifier = header.find(".//oai:identifier", NAMESPACES)
                if identifier is not None:
                    identifiers.append(identifier.text)

        token_elem = root.find(".//oai:resumptionToken", NAMESPACES)
        if token_elem is None or token_elem.text is None:
            break

        params = {"verb": "ListIdentifiers", "resumptionToken": token_elem.text}
    return identifiers


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _fetch_metadata(context: AssetExecutionContext, identifier: str):
    """
    Fetches metadata for a given identifier from the UK Data Service.

    Args:
        context (AssetExecutionContext): The execution context.
        identifier (str): The identifier for which to fetch metadata.

    Returns:
        ElementTree.Element: The root element of the fetched metadata XML.
    """
    metadata_url = (
        f"{BASE_URL}?verb=GetRecord&identifier={identifier}&metadataPrefix=ddi"
    )
    try:
        response = requests.get(metadata_url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        context.log.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        context.log.error(f"Other error occurred: {err}")
        raise

    return ET.fromstring(response.content)


@asset
def ukds_datasets(
    context: AssetExecutionContext, ukds_identifiers: list[str]
) -> pl.DataFrame:
    """
    Fetches datasets from the UK Data Service and returns them as a DataFrame.

    Args:
        context (AssetExecutionContext): The execution context.
        ukds_identifiers (list[str]): A list of identifiers.

    Returns:
        pl.DataFrame: A DataFrame containing the datasets.
    """
    data = []
    for identifier in tqdm(ukds_identifiers):
        context.log.info(f"Fetching identifier {identifier}")
        metadata = _fetch_metadata(context, identifier).find(
            ".//ns2:stdyDscr", NAMESPACES
        )

        if metadata is None:
            continue

        abstract = "\n".join(
            [
                re.sub("<[^<]+?>", "", m.text)
                for m in metadata.findall(".//ns2:abstract", NAMESPACES)
                if m.text is not None
            ]
        )
        date = metadata.find(".//ns2:depDate", NAMESPACES)
        title = metadata.find(".//ns2:titl", NAMESPACES)
        keywords = [
            m.text
            for m in metadata.findall(".//ns2:keyword", NAMESPACES)
            if m.text is not None
        ]
        doi = metadata.find(".//ns2:holdings", NAMESPACES)
        url = f"https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id={identifier}"
        data.append(
            {
                "title": title.text if title is not None else None,
                "abstract": abstract,
                "date": date.text if date is not None else None,
                "keywords": keywords,
                "doi": doi.get("URI") if doi is not None else None,
                "url": url,
            }
        )

    df = pl.DataFrame(data)
    df.write_parquet(Paths.UKDS / "ukds.parquet")
    return df


@asset
def ukds_abstracts(ukds_datasets: pl.DataFrame):
    """
    Extracts abstracts from the datasets and saves them as text files.

    Args:
        ukds_datasets (pl.DataFrame): A DataFrame containing the datasets.
    """
    outdir = Paths.UKDS / "txt"
    outdir.mkdir(parents=True, exist_ok=True)
    for file in outdir.glob("*.txt"):
        file.unlink()

    for row in ukds_datasets.rows(named=True):
        id = row["url"].split("=")[-1]
        abstract = row["abstract"].replace(
            "Abstract copyright UK Data Service and data collection copyright owner.",
            "",
        )
        with open(outdir / f"{id}-abstract.txt", "w") as f:
            f.write(clean_string(abstract))
