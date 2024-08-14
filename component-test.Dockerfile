# This file is used to run component tests on CI. Once the component tests don't rely on the common project, this
# file can be moved to a sub directory.
FROM python:3.9-slim-bullseye

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev swig pkg-config libxml2-dev libxslt-dev python3-dev libffi-dev

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /test
COPY . .

WORKDIR /test/integration-tests/integration_tests
ENV PYTHONPATH "${PYTHONPATH}:/test/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/test/common"

RUN pipenv --python 3.9
RUN pipenv install --dev --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "componenttests"]
