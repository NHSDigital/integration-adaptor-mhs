FROM python:3.11-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev swig pkg-config libxml2-dev libxslt-dev python3-dev libffi-dev

RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf # Temporarily lower security to workaround opentest certs with SHA1 signatures

RUN mkdir -p /usr/src/app/mhs/outbound

COPY mhs/outbound/Pipfile /usr/src/app
COPY mhs/outbound/Pipfile.lock /usr/src/app

RUN pip install --upgrade pip
RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/outbound/ /usr/src/app/mhs/outbound

WORKDIR /usr/src/app/mhs/outbound
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/common"

RUN pipenv --python 3.11
RUN pipenv install --deploy --ignore-pipfile

# PYCURL expects certificate to live in /etc/pki/tls, Debian is providing the cert in ssl/certs
RUN mkdir -p /etc/pki/tls && ln -s /etc/ssl/certs /etc/pki/tls/certs && ln -s ca-certificates.crt /etc/ssl/certs/ca-bundle.crt

EXPOSE 80

ENTRYPOINT ["pipenv", "run", "start"]
