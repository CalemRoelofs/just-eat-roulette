# Build package with poetry
FROM python:3.10 as builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 

RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./just_eat_roulette/ /code/just_eat_roulette/

RUN poetry build

# Create runtime using built package
FROM python:3.10-alpine as app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 

WORKDIR /app
RUN chown -R 1000 /app

COPY --from=builder /code/dist/*.whl /app

RUN apk add --no-cache build-base \ 
  && pip install -U setuptools pip \
  && find *.whl | xargs pip install --upgrade --force-reinstall

USER 1000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000 || exit 1

ENTRYPOINT [ "python", "-m", "just_eat_roulette.main" ]

