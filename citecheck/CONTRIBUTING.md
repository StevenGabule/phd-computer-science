# Contributing to CiteCheck

This is currently a solo research codebase associated with a PhD application
prep cycle (Fall 2028 entry). External contributions are welcome but not
expected during the build phase (Sep 2026 – Apr 2027); pull requests will be
reviewed best-effort.

## Development setup

```bash
git clone https://github.com/StevenGabule/phd-computer-science.git
cd phd-computer-science/citecheck

# Python 3.11+
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1

# Install with dev deps
pip install -e ".[dev]"

# Configure secrets (CourtListener key, HF token, wandb key)
cp .env.example .env
# Edit .env

# Verify
make info     # show configured paths
make test     # fast tests only (no network / GPU / large data)
```

## Code style

- Python 3.11+, type hints required on public APIs
- `ruff` for lint + format (config in `pyproject.toml`)
- `mypy --ignore-missing-imports` aspirationally clean
- One-line docstring required on every public function/class; longer where non-obvious
- `pathlib.Path`, not strings, for filesystem paths
- `logging` (module-level logger), not `print`, for status output
- Import config via `from citecheck.config import PATHS, MODELS, ...` — do not hardcode

Run `make lint && make fmt` before pushing.

## Tests

```bash
make test         # default: fast tests only (mocked external calls)
make test-all     # everything including slow/gpu/network tests (needs real env)
```

Tests are marked with pytest markers declared in `pyproject.toml`:

- `slow` — requires downloaded data (CAP, etc.)
- `gpu` — requires CUDA-capable GPU
- `network` — makes real HTTP calls

Default `make test` excludes all three so the suite is runnable on a fresh
checkout without setup.

## Commits and branches

- Main branch: `main`. Direct pushes to `main` allowed for the solo author;
  external contributors please open PRs.
- Commit messages: imperative present tense, body wrapped at ~72 chars.

## Reporting issues

Open an issue on the parent repo at
https://github.com/StevenGabule/phd-computer-science/issues with:

- What you tried
- What you expected
- What actually happened
- Environment (OS, Python version, GPU)
- Reproducible minimum example if possible

## Research-context PRs

If you're a researcher whose paper this work builds on (or potentially
diverges from), PRs that improve faithfulness to your method are especially
welcome — please cite the relevant section of your paper in the PR
description.
