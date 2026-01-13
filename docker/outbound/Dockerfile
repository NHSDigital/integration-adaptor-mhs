FROM python:3.11-slim-bookworm AS base

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential=12.9 \
       libssl-dev=3.0.18-1~deb12u1 \
       swig=4.1.0-0.2 \
       pkg-config=1.8.1-1 \
       libxml2-dev=2.9.14+dfsg-1.3~deb12u5 \
       libxslt1-dev=1.1.35-1+deb12u3 \
       python3-dev=3.11.2-1+b1 \
       libffi-dev=3.4.4-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf \
    && pip install --no-cache-dir --upgrade pip==25.3 \
    && pip install --no-cache-dir pipenv==2025.0.4

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/

WORKDIR /usr/src/app/mhs/outbound
ENV PYTHONPATH="/usr/src/app/mhs/common:/usr/src/app/common"

COPY mhs/outbound/Pipfile mhs/outbound/Pipfile.lock ./

RUN pipenv --python 3.11 \
    && pipenv install --deploy --ignore-pipfile

COPY mhs/outbound/ .

# PYCURL expects certificate to live in /etc/pki/tls, Debian is providing the cert in ssl/certs
RUN mkdir -p /etc/pki/tls \
    && ln -s /etc/ssl/certs /etc/pki/tls/certs \
    && ln -s ca-certificates.crt /etc/ssl/certs/ca-bundle.crt

EXPOSE 80
ENTRYPOINT ["pipenv", "run", "start"]
