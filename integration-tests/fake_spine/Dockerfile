FROM python:3.11-slim-bookworm
RUN apt-get update  \
    && apt-get install -y --no-install-recommends \
      build-essential=12.9 \
      git=1:2.39.5-0+deb12u2 \
      python3-dev=3.11.2-1+b1 \
      libffi-dev=3.4.4-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip==25.3 \
    && pip install --no-cache-dir pipenv==2025.0.4

WORKDIR /usr/src/app/mhs/fakespine
COPY common/ /usr/src/app/common/
COPY integration-tests/fake_spine/Pipfile .
COPY integration-tests/fake_spine/Pipfile.lock .

RUN pipenv install --deploy --system --ignore-pipfile

COPY integration-tests/fake_spine/ .

EXPOSE 80 443
ENTRYPOINT ["python", "main.py", "--logging=DEBUG"]