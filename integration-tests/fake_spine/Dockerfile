FROM python:3.11-slim-bookworm
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    git \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv
WORKDIR /usr/src/app/mhs/fakespine
COPY common/ /usr/src/app/common/
COPY integration-tests/fake_spine/Pipfile .
COPY integration-tests/fake_spine/Pipfile.lock .

RUN pipenv install --deploy --system --ignore-pipfile

COPY integration-tests/fake_spine/ .

EXPOSE 80 443
ENTRYPOINT ["python", "main.py", "--logging=DEBUG"]