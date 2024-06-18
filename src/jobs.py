from dagster import define_asset_job

adr_job = define_asset_job(
    "adr",
    selection=["adr_session", "adr_datasets_id", "adr_datasets", "adr_descriptions"],
)
pinecone_job = define_asset_job("pinecone", selection=["adr_pinecone"])
