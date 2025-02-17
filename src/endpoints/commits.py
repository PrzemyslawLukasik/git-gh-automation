import json
import os
from typing import Optional

from playwright.sync_api import APIRequestContext, APIResponse


class Commits:
    """Grouping class for commits API calls"""

    @staticmethod
    def get_commits(
        api_request_context: APIRequestContext, repo_name: str
    ) -> tuple[int, Optional[list[json]]]:
        response: APIResponse = api_request_context.get(
            f"/repos/{os.environ['USER']}/{repo_name}/commits"
        )
        if response.ok:
            return response.status, response.body
        else:
            return response.status, None
