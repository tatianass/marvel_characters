default:
  @just --list

# Initialize the local environment
init PY_VERSION='3.13':
    uv venv --python {{PY_VERSION}}
    uv tool install ruff
    uv tool install bandit
    pre-commit install

# Update the precommit
update:
    pre-commit autoupdate

# Delete all temporary files
clean:
    rm -rf .ipynb_checkpoints
    rm -rf **/.ipynb_checkpoints
    rm -rf .pytest_cache
    rm -rf **/.pytest_cache
    rm -rf __pycache__
    rm -rf **/__pycache__
    rm -rf build
    rm -rf dist

# Build the Docker image
build:
    docker build . -t marvel_characters


# Launch the full stack
run:
    python3 -m marvel_characters.main

# Launch the full stack
run-full:
    docker compose up --build --exit-code-from marvel_characters

# Install for production
install:
    uv sync

# Generate requirements
compile:
	uv pip compile pyproject.toml -o requirements.txt

# Check linting, formatting compliance and common security issues
check:
    uv tool run ruff check
    uv tool run bandit -r src/

# Format files using ruff
format:
    uv tool run ruff check --fix
    uv tool run ruff format

# Run tests
test:
    uv run pytest --cov=src --log-level=WARNING --disable-pytest-warnings

# Run tests
test-docker:
    docker compose -f compose.test.yml up -d

# Run pre-commit hooks without commiting
pre-commit:
    pre-commit run --all-files

alias fix := pre-commit
