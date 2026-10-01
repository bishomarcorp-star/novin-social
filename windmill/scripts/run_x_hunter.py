# Windmill entrypoint for Novin Social X Hunter.
# Expected environment:
# NOVIN_SOCIAL_API_BASE_URL=http://api:8000
# PROJECT_ID=1

import os
import requests


def main(project_id: int | None = None, post_limit: int = 20, replies_per_post: int = 100):
    api_base = os.environ.get("NOVIN_SOCIAL_API_BASE_URL", "http://api:8000").rstrip("/")
    project_id = project_id or int(os.environ.get("PROJECT_ID", "1"))

    response = requests.post(
        f"{api_base}/hunter-jobs/x/run",
        json={
            "project_id": project_id,
            "post_limit": post_limit,
            "replies_per_post": replies_per_post,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()
