# Python Starter Template

This is a simple python backend template for starting a new project.
It includes a project structure, a crud API example, and a Dockerfile for containerization.

## What's included

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - A micro web framework written in Python.
- [SQLAlchemy](https://www.sqlalchemy.org/) - A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using Python type annotations.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - A lightweight database migration tool for SQLAlchemy.

## Getting started

## Prerequisites

- [Astral UV](https://docs.astral.sh/uv/)
- [Python 3.13](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the project

### Running the project with docker compose

```bash
docker compose up
```

### Running the project with Astral UV

> IMPORTANT: Make sure you have a database up and running on your local machine.
> Postgres needs to be running on port 5432.

```bash
uv run python main.py
```

### Running the migrations

```bash
uv run alembic upgrade head
```
