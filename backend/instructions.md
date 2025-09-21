# Testing Guide for Voice Marketing Agents

## Quick Start

1. **Setup (one-time):**
   ```bash
   cd backend
   python setup_tests.py
   ```

2. **Run tests:**
   ```bash
   pytest
   ```

## Available Commands

- `make test` - Run all tests
- `make test-unit` - Run unit tests only  
- `make test-coverage` - Run tests with coverage report
- `make lint` - Check code quality
- `make format` - Format code

## Test Structure

- `tests/test_models/` - Database model tests
- `tests/test_services/` - AI service tests  
- `tests/test_api/` - API endpoint tests
- `tests/test_agents/` - Agent logic tests

## Writing New Tests

1. Add test files with `test_` prefix
2. Use provided fixtures from `conftest.py`
3. Mock external services (LLM, STT, TTS)
4. Follow existing test patterns

## Coverage Requirements

- Minimum 80% code coverage
- All new features must include tests
- Critical paths must be tested

## Troubleshooting

If tests fail:
1. Check you're in the `backend/` directory
2. Ensure dependencies are installed: `pip install -r requirements-dev.txt`
3. Check that main application runs: `python -m src.main`
#!/bin/bash

# Test runner script for CI/CD

set -e

echo "🧪 Starting Voice Marketing Agents Test Suite"
echo "=============================================="

# Check if we're in a virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "⚠️  Warning: Not running in a virtual environment"
fi

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -r requirements-dev.txt

# Run code formatting checks
echo "🎨 Checking code formatting..."
black --check src tests || {
    echo "❌ Code formatting issues found. Run 'make format' to fix."
    exit 1
}

# Run import sorting checks
echo "📚 Checking import sorting..."
isort --check-only src tests || {
    echo "❌ Import sorting issues found. Run 'make format' to fix."
    exit 1
}

# Run linting
echo "🔍 Running linting..."
flake8 src tests || {
    echo "❌ Linting issues found."
    exit 1
}

# Run unit tests
echo "⚡ Running unit tests..."
pytest tests/ -v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=80

echo ""
echo "✅ All tests passed!"
echo "📊 Coverage report generated in htmlcov/"
echo "🎉 Voice Marketing Agents is ready for deployment!"