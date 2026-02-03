FROM python:3.11-slim-bookworm AS base

RUN apt-get update  \
    && apt-get install -y --no-install-recommends \
       build-essential=12.9 \
       libssl-dev=3.0.18-1~deb12u2 \
       libffi-dev=3.4.4-1 \
       libxml2-dev=2.9.14+dfsg-1.3~deb12u5 \
       libxslt1-dev=1.1.35-1+deb12u3 \
       pkg-config=1.8.1-1 \
       python3-dev=3.11.2-1+b1 \
       swig=4.1.0-0.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf \
    && mkdir -p /usr/src/app/mhs/inbound \
    && pip install --no-cache-dir --upgrade pip==25.3 \
    && pip install --no-cache-dir pipenv==2025.0.4

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/inbound/ /usr/src/app/mhs/inbound

WORKDIR /usr/src/app/mhs/inbound
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app/common"

RUN pipenv --python 3.11 \
    && pipenv install --deploy --ignore-pipfile

EXPOSE 443 80

ENTRYPOINT ["pipenv", "run", "start"]
