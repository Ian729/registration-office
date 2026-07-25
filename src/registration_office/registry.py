from __future__ import annotations

from typing import Any

import yaml

from .parser import RegistrationRequest


def register_project(content: str, request: RegistrationRequest) -> tuple[str, bool]:
    document: dict[str, Any] = yaml.safe_load(content) or {"version": 1, "projects": []}
    if document.get("version") != 1 or not isinstance(document.get("projects"), list):
        raise ValueError("unsupported projects.yaml format")

    projects: list[dict[str, Any]] = document["projects"]
    for project in projects:
        if project.get("name") == request.name:
            if project.get("repo") == request.project_url:
                return content, False
            raise ValueError(f"project name already registered: {request.name}")
        if project.get("repo") == request.project_url:
            raise ValueError(f"project URL already registered as {project.get('name')}")

    projects.append({
        "name": request.name,
        "repo": request.project_url,
        "revision": "main",
        "enabled": True,
    })
    projects.sort(key=lambda item: str(item.get("name", "")).lower())
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=True), True
