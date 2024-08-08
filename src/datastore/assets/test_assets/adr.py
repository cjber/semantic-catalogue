import polars as pl
from dagster import AssetCheckResult, asset_check

from src.common.utils import Paths


@asset_check(asset="adr_datasets_id")
def adr_datasets_id_no_nulls():
    adr_datasets_id = pl.read_parquet(Paths.ADR / "adr_datasets_id.parquet")
    num_nulls = adr_datasets_id.null_count().sum_horizontal()[0]
    return AssetCheckResult(passed=bool(num_nulls == 0))
