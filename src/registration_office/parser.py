from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class RegistrationRequest:
    name: str
    project_url: str


_FIELD_PATTERNS = {
    "name": re.compile(r"^\s*(?:[-*]\s*)?(?:name|project\s*name)\s*[:：]\s*(.+?)\s*$", re.I | re.M),
    "project_url": re.compile(r"^\s*(?:[-*]\s*)?(?:project\s*url|repo(?:sitory)?\s*url|url)\s*[:：]\s*(\S+)\s*$", re.I | re.M),
}


def parse_registration_request(body: str) -> RegistrationRequest:
    values: dict[str, str] = {}
    for field, pattern in _FIELD_PATTERNS.items():
        match = pattern.search(body or "")
        if not match:
            raise ValueError(f"missing required field: {field}")
        values[field] = match.group(1).strip()

    name = values["name"]
    project_url = values["project_url"].removesuffix("/")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", name):
        raise ValueError("name must contain only letters, numbers, '.', '_' or '-'")

    parsed = urlparse(project_url)
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        raise ValueError("project_url must be an https://github.com/... repository URL")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2:
        raise ValueError("project_url must point to a GitHub repository")

    return RegistrationRequest(name=name, project_url=project_url + (".git" if not project_url.endswith(".git") else ""))
