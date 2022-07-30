FROM python:3.10

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

COPY ./backend/ /code/

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000 || exit 1

ENTRYPOINT [ "poetry", "run", "python", "main.py" ]

