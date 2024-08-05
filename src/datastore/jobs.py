from dagster import define_asset_job

adr_job = define_asset_job(
    "adr",
    selection=["adr_session", "adr_datasets_id", "adr_datasets", "adr_descriptions"],
)
ukds_job = define_asset_job(
    "ukds",
    selection=["ukds_identifiers", "ukds_datasets", "ukds_abstracts"],
)
cdrc_job = define_asset_job(
    "cdrc",
    selection=[
        "cdrc_session",
        "cdrc_metadata",
        "cdrc_notes",
        "cdrc_resources",
        "cdrc_pdfs",
    ],
)
