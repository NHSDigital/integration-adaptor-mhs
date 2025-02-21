FROM python:3.13-slim-bookworm
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    git \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/src/app/mhs/fakespine
RUN pip install pipenv
COPY common/ /usr/src/app/common/
COPY integration-tests/fake_spine/ /usr/src/app/mhs/fakespine
WORKDIR /usr/src/app/mhs/fakespine
COPY integration-tests/fake_spine/Pipfile /usr/src/app
COPY integration-tests/fake_spine/Pipfile.lock /usr/src/app

RUN pipenv --python 3.13
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

COPY . .
EXPOSE 80 443
ENTRYPOINT ["pipenv", "run", "start", "--logging=DEBUG"]
