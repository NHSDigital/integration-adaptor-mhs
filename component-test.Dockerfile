# This file is used to run component tests on CI. Once the component tests don't rely on the common project, this
# file can be moved to a sub directory.
FROM python:3.8-slim-bullseye

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev swig pkg-config
RUN pip install pipenv

WORKDIR /test
COPY . .

WORKDIR /test/integration-tests/integration_tests
ENV PYTHONPATH "${PYTHONPATH}:/test/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/test/common"

RUN pipenv --python 3.8
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --dev --deploy --ignore-pipfile

ENTRYPOINT pipenv run componenttests
