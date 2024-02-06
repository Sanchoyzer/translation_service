PROJ_PATH       ?= app
TESTS_PATH      ?= tests
MIGRATION_PATH  ?= migrations

DC              ?= docker compose

### linters ###

.PHONY: black
black:
	black ${PROJ_PATH} ${TESTS_PATH} ${MIGRATION_PATH}

.PHONY: ruff
ruff:
	ruff ${PROJ_PATH} ${TESTS_PATH} ${MIGRATION_PATH}

.PHONY: ruff_fix
ruff_fix:
	ruff --fix ${PROJ_PATH} ${TESTS_PATH} ${MIGRATION_PATH}

.PHONY: mypy
mypy:
	mypy ${PROJ_PATH} ${TESTS_PATH}

.PHONY: bandit
bandit:
	bandit -c pyproject.toml --silent -r ${PROJ_PATH}

.PHONY: check
check: black ruff mypy bandit

### tests ###

.PHONY: tests
tests:
	pytest --cov-report term-missing --cov=app --durations=3
	pytest --dead-fixtures

### poerty wrappers ###

.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update


### local dev ###

.PHONY: up
up:
	${DC} up --build -d


.PHONY: up_live
up_live:
	${DC} up --build


.PHONY: up_db
up_db:
	${DC} up --build -d mongo


.PHONY: down
down:
	${DC} down


.PHONY: logs
logs:
	${DC} logs -f -n 200


### migrations ###


.PHONY: migration_create
migration_create:
	mongodb-migrate-create --description initial


.PHONY: migration_upgrade
migration_upgrade:
	mongodb-migrate --url 'mongodb://localhost:27017/test'
