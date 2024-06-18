from dagster import Definitions, load_assets_from_modules

from src.assets import adr, datastore
from src.jobs import adr_job
from src.resources import openai_resource

adr_assets = load_assets_from_modules(modules=[adr], group_name="adr_assets")
datastore_assets = load_assets_from_modules(modules=[datastore], group_name="datastore")

defs = Definitions(
    assets=[*adr_assets, *datastore_assets],
    jobs=[adr_job],
    resources={"openai": openai_resource},
)
