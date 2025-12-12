# This file is used to run component tests on CI. Once the component tests don't rely on the common project, this
# file can be moved to a sub directory.
FROM python:3.11-slim-bookworm

RUN apt-get update  \
    && apt-get install -y --no-install-recommends \
      build-essential=12.9 \
      libssl-dev=3.0.17-1~deb12u3 \
      swig=4.1.0-0.2 \
      pkg-config=1.8.1-1 \
      libxml2-dev=2.9.14+dfsg-1.3~deb12u4 \
      libxslt1-dev=1.1.35-1+deb12u3 \
      python3-dev=3.11.2-1+b1 \
      libffi-dev=3.4.4-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip==25.3 \
    && pip install --no-cache-dir pipenv==2025.0.4

WORKDIR /test
COPY . .

WORKDIR /test/integration-tests/integration_tests
ENV PYTHONPATH "${PYTHONPATH}:/test/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/test/common"

RUN pipenv --python 3.11 \
    && pipenv install --dev --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "componenttests"]
