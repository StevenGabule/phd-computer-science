# CiteCheck — common dev commands. Run from citecheck/ directory.
# Usage: make <target>

PY ?= python
PIP ?= pip
PYTEST_FAST_MARKERS := not slow and not gpu and not network

.PHONY: help install install-dev test test-fast test-all lint fmt mypy clean info

help: ## Show this help
	@echo "CiteCheck dev commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package (runtime deps only)
	$(PIP) install -e .

install-dev: ## Install package + dev deps (pytest, ruff, mypy)
	$(PIP) install -e ".[dev]"

test test-fast: ## Run fast tests only (excludes slow/gpu/network markers)
	pytest -m "$(PYTEST_FAST_MARKERS)" -v

test-all: ## Run all tests including slow/gpu/network (requires real data + API keys)
	pytest -v

lint: ## Lint with ruff
	ruff check src tests

fmt: ## Auto-format code with ruff
	ruff format src tests
	ruff check --fix src tests

mypy: ## Type-check with mypy (best-effort)
	mypy src --ignore-missing-imports

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

info: ## Show citecheck CLI configured paths
	$(PY) -m citecheck.cli info
