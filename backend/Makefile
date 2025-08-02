.PHONY: test test-unit test-integration test-coverage lint format install-dev

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run all tests
test:
	pytest

# Run only unit tests
test-unit:
	pytest -m "not integration and not slow"

# Run integration tests
test-integration:
	pytest -m integration

# Run tests with coverage report
test-coverage:
	pytest --cov=src --cov-report=html --cov-report=term

# Lint code
lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

# Format code
format:
	black src tests
	isort src tests

# Run tests in watch mode (requires pytest-xdist)
test-watch:
	pytest --looponfail

# Clean up test artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete