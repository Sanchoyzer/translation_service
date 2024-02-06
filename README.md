![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Sanchoyzer/translation_service)
![GitHub last commit](https://img.shields.io/github/last-commit/Sanchoyzer/translation_service)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?logo=githubactions&logoColor=white)](https://github.com/Sanchoyzer/translation_service/actions)
[![Sentry](https://img.shields.io/static/v1?message=Sentry&color=362D59&logo=Sentry&logoColor=FFFFFF&label=)](https://sentry.io)

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

## Translation Service ##

Web service with REST API to get Google translation

Technologies and libraries: python, fastapi, mongodb, motor, mongodb-migrations, gunicorn, sentry, docker, pytest, linters

### Technologies ###

- [python](https://www.python.org/)
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [poetry](https://python-poetry.org/docs/)
- [make](https://www.gnu.org/software/make/)

### How to ... ###

#### ... run application ####
`make up`

#### ... stop application ####
`make down`

#### ... run tests ####
`make tests`

#### ... run linters ####
`make check`

#### ... find Swagger UI ####
[Swagger UI](http://0.0.0.0:8081/docs)

---

## Original task

### Translation Service Challenge

### Goal
The goal of this challenge is to create a microservice providing a JSON API to work with word
definitions/translations taken from Google Translate. Note that support of anything longer than a single
word is not required.

### Endpoints
- Get the details about the given word.
The response shall include definitions, synonyms, translations and examples
(e.g. [challenge word translation](https://translate.google.com/details?sl=en&tl=es&text=challenge&op=translate)).
Data fetched from Google Translate has to be saved in the DB. When a request arrives to the endpoint,
the handler has to look for the word in the DB first and fall back to Google Translate only if it is not there.
- Get the list of the words stored in the database.
Pagination, sorting and filtering by word is required. Partial match has to be used for filtering.
Definitions, synonyms and translations shall not be included in the response by default but can be
enabled by providing corresponding query parameters.
- Delete a word from the database.

### Non functional requirements
- Python 3
- FastAPI in async mode
- Dockerfile and docker-compose.yml have to be included
- NoSQL database
- Authentication is not required
