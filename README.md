# marvel_characters
This project aims to provide a solution for a project interview related to the presence of Marvel characters in
different comics.

## Prerequisites

- `just`: [see here](https://github.com/cajsey/just) `brew install just`
- `python3` (>=3.10 preferred)
- `uv` [see here](https://github.com/astral-sh/uv)
- `pre-commit`: `brew install pre-commit`
- `docker`

Activate the virtual environment with :
```bash
source .venv/bin/activate
```

## Project structure

```text
.
├── Dockerfile
├── README.md
├── compose.yml
├── justfile
├── pyproject.toml
│   └── ...
├── src
│   └── marvel_characters
│       ├── __init__.py
│       └── main.py
│       └── character.py
└── tests
    └── test_marvel_characters.py
```

This project is structured using a `src` layout and is composed of
different components.

- `Dockerfile`: building instructions for Docker.
- `README.md`: this file.
- `compose*.yml`: `docker compose` configuration to run and test the
  project locally.
- `justfile`: Preconfigured list of commands using `just` ([see here](https://github.com/cajsey/just))
- `pyproject.toml`: Python project configuration (dependencies, dev
  tools setup and more)
- `scripts`: Useful scripts for development or deployment.
- `src`: Package code.
- `tests`: Tests code.

## Setup

Activate the virtual environment with :

```bash
source .venv/bin/activate
```

Don't forget to create the `.env.local` file with the credentials needed.

Check the `justfile` for all the available commands.
