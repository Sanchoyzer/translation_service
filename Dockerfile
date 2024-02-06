FROM python:3.11.7-slim as base
RUN python -m pip install --upgrade --no-cache-dir pip wheel setuptools \
    && python -m pip install poetry \
    && poetry config virtualenvs.create false \
    && mkdir -p /srv/src

ENV PYTHONPATH=/srv/src
WORKDIR /srv/src

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --only=main  \
    && rm -rf /root/.cache

COPY app ./app


FROM base as development
CMD uvicorn --factory app.main:init_app --host 0.0.0.0 --port 8080 --reload


FROM base as test
RUN poetry install --only=test
COPY ../tests ./tests
CMD python -m pytest --cov-report term-missing --cov=app --durations=3 .


FROM base as production
CMD gunicorn "app.main:init_app()" --timeout 120 --workers $(nproc) --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --log-file -
