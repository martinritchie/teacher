.PHONY: format lint fix check help install reinstall clean test test-functional test-all coverage

help:
	@echo "Teacher - ML papers to podcast-style audio, with local models"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make reinstall   Clean and reinstall dependencies"
	@echo "  make clean       Remove build artifacts and cache files"
	@echo "  make format      Format code with ruff"
	@echo "  make lint        Check code quality"
	@echo "  make check       Format, lint and typecheck"
	@echo "  make test             Unit tests: under 2 seconds, offline, no GPU"
	@echo "  make test-functional  Functional tests: real MinerU, Qwen3-TTS, tokenizer and processes (minutes, GPU)"
	@echo "  make test-all         Both"
	@echo "  make coverage         Unit tests with a coverage report (terminal, and htmlcov/index.html)"
	@echo "  make help        Show this help message"

install:
	uv sync --all-extras

reinstall:
	rm -rf .venv
	uv sync

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .ruff_cache build dist *.egg-info .coverage htmlcov 2>/dev/null || true

format:
	uv run ruff format .

lint:
	uv run ruff check --fix .
	uv run ty check

check: format lint
	@echo "✓ Code formatting and linting complete"

test:
	uv run pytest

test-functional:
	uv run pytest -m functional

test-all:
	uv run pytest -m ""

coverage:
	uv run pytest --cov=teacher --cov-report=term-missing --cov-report=html
