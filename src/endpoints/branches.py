import json
import os
from typing import Optional

from playwright.sync_api import APIRequestContext, APIResponse


class Branches:
    @staticmethod
    def get_branches(
        api_request_context: APIRequestContext, repo_name: str
    ) -> tuple[int, Optional[list]]:
        response: APIResponse = api_request_context.get(
            f"/repos/{os.environ['API_USER']}/{repo_name}/branches"
        )
        if response.ok:
            return response.status, response
        else:
            return response.status, None

    @staticmethod
    def get_branches_list(
        api_request_context: APIRequestContext, repo_name: str
    ) -> list[dict]:
        _, response = Branches().get_branches(api_request_context, repo_name)
        list_of_branches = response.json()
        return list_of_branches

    @staticmethod
    def merge_branches(
        api_request_context: APIRequestContext,
        repo_name: str,
        root_branch: str,
        feature_branch: str,
        commit_message: str,
    ) -> None:
        payload = {
            "base": f"{root_branch}",
            "head": f"{feature_branch}",
            "commit_message": commit_message,
        }
        response: APIResponse = api_request_context.post(
            f"/repos/{os.environ['API_USER']}/{repo_name}/merges", data=payload
        )
        return response
