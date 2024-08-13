FROM python:3.9-slim-bullseye AS base

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 80
ENTRYPOINT ["pipenv", "run", "start", "--logging=DEBUG"]
