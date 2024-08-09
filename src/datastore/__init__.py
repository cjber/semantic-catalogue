from dagster import Definitions, load_assets_from_modules

from src.datastore.assets import adr, cdrc, datastore, ukds
# from src.datastore.assets.test_assets.adr import adr_datasets_id_no_nulls
from src.datastore.jobs import adr_job, cdrc_job, ukds_job
from src.datastore.resources import openai_resource
from src.datastore.schedules import adr_schedule, cdrc_schedule, ukds_schedule

adr_assets = load_assets_from_modules(modules=[adr], group_name="adr_assets")
ukds_assets = load_assets_from_modules(modules=[ukds], group_name="ukds_assets")
cdrc_assets = load_assets_from_modules(modules=[cdrc], group_name="cdrc_assets")
datastore_assets = load_assets_from_modules(modules=[datastore], group_name="datastore")

defs = Definitions(
    assets=[*ukds_assets, *adr_assets, *cdrc_assets, *datastore_assets],
    # asset_checks=[adr_datasets_id_no_nulls],
    jobs=[adr_job, ukds_job, cdrc_job],
    schedules=[adr_schedule, ukds_schedule, cdrc_schedule],
    resources={"openai": openai_resource},
)
