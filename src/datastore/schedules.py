from dagster import DefaultScheduleStatus, ScheduleDefinition

from src.datastore.jobs import adr_job, cdrc_job, ukds_job

adr_schedule = ScheduleDefinition(
    job=adr_job,
    cron_schedule="0 0 * * 0",
    name="adr_weekly_schedule",
    default_status=DefaultScheduleStatus.RUNNING,
)
cdrc_schedule = ScheduleDefinition(
    job=cdrc_job,
    cron_schedule="0 0 * * 0",
    name="cdrc_weekly_schedule",
    default_status=DefaultScheduleStatus.RUNNING,
)
ukds_schedule = ScheduleDefinition(
    job=ukds_job,
    cron_schedule="0 0 * * 0",
    name="ukds_weekly_schedule",
    default_status=DefaultScheduleStatus.RUNNING,
)
