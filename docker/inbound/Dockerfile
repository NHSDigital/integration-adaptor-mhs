FROM python:3.9-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev swig pkg-config libxml2-dev libxslt-dev python3-dev libffi-dev

RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf # Temporarily lower security to workaround opentest certs with SHA1 signatures

RUN mkdir -p /usr/src/app/mhs/inbound

RUN pip install --upgrade pip
RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/inbound/ /usr/src/app/mhs/inbound

WORKDIR /usr/src/app/mhs/inbound
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/common"

RUN pipenv --python 3.9
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 443 80

ENTRYPOINT ["pipenv", "run", "start"]
