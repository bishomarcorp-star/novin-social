# Windmill orchestration

This directory contains job entrypoints for Novin Social orchestration.

## X Hunter job

Script:
- `scripts/run_x_hunter.py`

Environment:
- `NOVIN_SOCIAL_API_BASE_URL`
- `PROJECT_ID`

The job calls Novin Social's internal API:
- `POST /hunter-jobs/x/run`

Secrets such as `X_BEARER_TOKEN` belong to the Novin Social API runtime environment and are never committed to the repository.
