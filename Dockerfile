FROM python:3.9.5-slim

RUN pip install poetry

RUN mkdir /app
RUN mkdir /config

COPY /src /app/src
COPY pyproject.toml /app

WORKDIR /app

RUN poetry build

WORKDIR /app/dist

RUN pip install aria_backend-0.1.0.tar.gz

CMD ["aria-backend" , "-c", "/config/config.json"]