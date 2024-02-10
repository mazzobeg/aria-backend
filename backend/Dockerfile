FROM python:3.10.12-slim

RUN mkdir /app

COPY /dist/aria_backend-0.1.0.tar.gz /app
COPY /config/docker.py /app

WORKDIR /app

RUN pip install aria_backend-0.1.0.tar.gz
RUN rm aria_backend-0.1.0.tar.gz

CMD ["aria-backend", "-c", "/app/docker.py"]