from dagster import Definitions, load_assets_from_modules

from semantic_catalogue.datastore.assets import adr, cdrc, datastore, ukds
from semantic_catalogue.datastore.jobs import adr_job, cdrc_job, ukds_job
from semantic_catalogue.datastore.resources import openai_resource
from semantic_catalogue.datastore.schedules import (
    adr_schedule,
    cdrc_schedule,
    ukds_schedule,
)

adr_assets = load_assets_from_modules(modules=[adr], group_name="adr_assets")
ukds_assets = load_assets_from_modules(modules=[ukds], group_name="ukds_assets")
cdrc_assets = load_assets_from_modules(modules=[cdrc], group_name="cdrc_assets")
datastore_assets = load_assets_from_modules(modules=[datastore], group_name="datastore")

defs = Definitions(
    assets=[*ukds_assets, *adr_assets, *cdrc_assets, *datastore_assets],
    jobs=[adr_job, ukds_job, cdrc_job],
    schedules=[adr_schedule, ukds_schedule, cdrc_schedule],
    resources={"openai": openai_resource},
)
