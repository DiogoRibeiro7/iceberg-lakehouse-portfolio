# Contributing

## Development setup

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -e .[dev]
```

4. Start local services when needed:

```bash
docker compose -f docker/docker-compose.yml up -d
```

## Branching and commits

1. Create feature branches from `develop`.
2. Keep commit messages in Conventional Commits style.
3. Keep pull requests focused and small when possible.

Examples:
- `feat(sql): add partition evolution demo`
- `fix(pipeline): handle invalid order date`
- `docs(readme): clarify local setup`

## Quality checks

Run before opening a PR:

```bash
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy src tests
python -m pytest -q
```

Optional smoke validation:

```bash
python scripts/smoke_test.py --config-profile config/profiles/local.env
```

## Pull request guidelines

1. Link the related issue if one exists.
2. Describe problem, solution, and validation clearly.
3. Update docs/tests when behavior changes.
4. Ensure CI passes before requesting review.
