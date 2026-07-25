from __future__ import annotations

import os
from dataclasses import dataclass

from github import Auth, Github
from github.GithubException import GithubException

from .parser import parse_registration_request
from .registry import register_project


@dataclass(frozen=True)
class Settings:
    station_repo: str = "Ian729/train-station"
    registry_path: str = "projects.yaml"
    request_label: str = "train-registration"
    success_label: str = "train-registered"
    failure_label: str = "train-registration-failed"


def run(settings: Settings | None = None) -> int:
    settings = settings or Settings(
        station_repo=os.getenv("TRAIN_STATION_REPO", "Ian729/train-station"),
        registry_path=os.getenv("TRAIN_STATION_REGISTRY", "projects.yaml"),
        request_label=os.getenv("REGISTRATION_REQUEST_LABEL", "train-registration"),
        success_label=os.getenv("REGISTRATION_SUCCESS_LABEL", "train-registered"),
        failure_label=os.getenv("REGISTRATION_FAILURE_LABEL", "train-registration-failed"),
    )
    token = os.environ["GITHUB_TOKEN"]
    repo = Github(auth=Auth.Token(token)).get_repo(settings.station_repo)
    failures = 0

    for issue in repo.get_issues(state="open", labels=[settings.request_label]):
        labels = {label.name for label in issue.labels}
        if settings.success_label in labels:
            continue
        try:
            request = parse_registration_request(issue.body or "")
            current = repo.get_contents(settings.registry_path)
            current_text = current.decoded_content.decode("utf-8")
            updated_text, changed = register_project(current_text, request)
            if changed:
                repo.update_file(
                    settings.registry_path,
                    f"Register train: {request.name}",
                    updated_text,
                    current.sha,
                    branch=repo.default_branch,
                )
            issue.add_to_labels(settings.success_label)
            if settings.failure_label in labels:
                issue.remove_from_labels(settings.failure_label)
            issue.create_comment(
                f"✅ Registered `{request.name}` from `{request.project_url}` in `{settings.registry_path}`."
                if changed else
                f"✅ `{request.name}` was already registered with the same project URL."
            )
        except (ValueError, GithubException, KeyError) as exc:
            failures += 1
            issue.add_to_labels(settings.failure_label)
            issue.create_comment(f"❌ Registration failed: `{exc}`")

    return 1 if failures else 0
