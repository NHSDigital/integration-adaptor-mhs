FROM python:3.11-slim-bookworm AS base

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libssl-dev \
    swig \
    pkg-config \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    libffi-dev  \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf \
    && pip install --upgrade pip \
    && pip install pipenv

WORKDIR /usr/src/app/mhs/outbound
ENV PYTHONPATH="/usr/src/app/mhs/common:/usr/src/app/common"

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/

COPY mhs/outbound/Pipfile .
COPY mhs/outbound/Pipfile.lock .

RUN pipenv --python 3.11 \
    && pipenv install --deploy --ignore-pipfile

COPY mhs/outbound/ .

# PYCURL expects certificate to live in /etc/pki/tls, Debian is providing the cert in ssl/certs
RUN mkdir -p /etc/pki/tls \
    && ln -s /etc/ssl/certs /etc/pki/tls/certs \
    && ln -s ca-certificates.crt /etc/ssl/certs/ca-bundle.crt

EXPOSE 80
ENTRYPOINT ["pipenv", "run", "start"]
