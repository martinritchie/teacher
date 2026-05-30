.PHONY: format lint fix check help install reinstall clean test

help:
	@echo "Teacher - Research paper to audio transcript system"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make reinstall   Clean and reinstall dependencies"
	@echo "  make clean       Remove build artifacts and cache files"
	@echo "  make format      Format code with ruff"
	@echo "  make lint        Check code quality"
	@echo "  make check       Format and lint"
	@echo "  make test        Run the test suite"
	@echo "  make help        Show this help message"

install:
	uv sync --all-extras

reinstall:
	rm -rf .venv
	uv sync

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .ruff_cache build dist *.egg-info 2>/dev/null || true

format:
	uv run ruff format .

lint:
	uv run ruff check --fix .

check: format lint
	@echo "✓ Code formatting and linting complete"

test:
	uv run pytest
