# Registration Office

Registration Office is the first external Train Station project.

It reads issues from `Ian729/train-station`, selects issues carrying the `train-registration` label, parses the requested project name and repository URL, updates `projects.yaml`, and marks successful requests with `train-registered`.

## Issue format

```text
name: example-project
project url: https://github.com/example/example-project
```

## Labels

- `train-registration`: pending registration request
- `train-registered`: registration completed
- `train-registration-failed`: validation or update failed

## Train Station entrypoint

```text
.trainstation/run.sh
```

The script expects a GitHub token in `GITHUB_TOKEN`. The token must be able to read issues and update files, labels, and issue comments in `Ian729/train-station`.

## Local development

```bash
python -m pip install -e '.[dev]'
pytest
```

## Behavior

1. Find open issues labeled `train-registration`.
2. Parse `name` and `project url` from the issue body.
3. Validate the project name and GitHub repository URL.
4. Add the project to `projects.yaml` unless already registered.
5. Commit the registry update through the GitHub Contents API.
6. Add `train-registered` and post a success comment.
7. On failure, add `train-registration-failed` and post the error.

## License

MIT
