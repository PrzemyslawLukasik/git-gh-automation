import os
from typing import Optional

from playwright.sync_api import APIRequestContext, APIResponse


class Repositories:
    """Grouping class for Repositories based API calls"""

    @staticmethod
    def user_repositories_list(
        api_request_context: APIRequestContext,
    ) -> tuple[int, Optional[APIResponse]]:
        response: APIResponse = api_request_context.get(
            f"/users/{os.environ['API_USER']}/repos"
        )
        if response.ok:
            return response.status, response
        else:
            return response.status, None

    @staticmethod
    def create_repository(
        api_request_context: APIRequestContext, data: dict
    ) -> tuple[int, Optional[tuple[int, str]]]:
        response: APIResponse = api_request_context.post("/user/repos", data=data)
        if response.ok:
            return response.status, response.json()["name"]
        else:
            return response.status, None

    @staticmethod
    def delete_repository(api_request_context: APIRequestContext, name: str) -> int:
        response: APIResponse = api_request_context.delete(
            f"/repos/{os.environ['USER']}/{name}"
        )
        return response.status
