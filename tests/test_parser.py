import pytest

from registration_office.parser import parse_registration_request


def test_parse_request():
    request = parse_registration_request(
        "name: demo\nproject url: https://github.com/acme/demo"
    )
    assert request.name == "demo"
    assert request.project_url == "https://github.com/acme/demo.git"


def test_reject_non_github_url():
    with pytest.raises(ValueError):
        parse_registration_request(
            "name: demo\nproject url: https://example.com/demo"
        )
