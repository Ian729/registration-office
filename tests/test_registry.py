import yaml

from registration_office.parser import RegistrationRequest
from registration_office.registry import register_project


def test_register_project():
    updated, changed = register_project(
        "version: 1\nprojects: []\n",
        RegistrationRequest("demo", "https://github.com/acme/demo.git"),
    )
    assert changed is True
    assert yaml.safe_load(updated)["projects"][0]["name"] == "demo"


def test_idempotent_registration():
    content = (
        "version: 1\nprojects:\n"
        "  - name: demo\n"
        "    repo: https://github.com/acme/demo.git\n"
    )
    updated, changed = register_project(
        content,
        RegistrationRequest("demo", "https://github.com/acme/demo.git"),
    )
    assert changed is False
    assert updated == content
