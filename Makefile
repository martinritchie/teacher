.PHONY: format lint fix check help install reinstall clean test test-all coverage

help:
	@echo "Teacher - ML papers to podcast-style audio, with local models"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make reinstall   Clean and reinstall dependencies"
	@echo "  make clean       Remove build artifacts and cache files"
	@echo "  make format      Format code with ruff"
	@echo "  make lint        Check code quality"
	@echo "  make check       Format and lint"
	@echo "  make test        Run the fast tests (stub models; MinerU on the GPU once)"
	@echo "  make test-all    Also run the slow test, which loads real Qwen3-TTS"
	@echo "  make coverage    Run the fast tests with a coverage report (terminal, and htmlcov/index.html)"
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

check: format lint
	@echo "✓ Code formatting and linting complete"

test:
	uv run pytest -m "not slow"

test-all:
	uv run pytest

coverage:
	uv run pytest -m "not slow" --cov=teacher --cov-report=term-missing --cov-report=html
