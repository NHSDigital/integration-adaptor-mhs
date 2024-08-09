FROM python:3.7-slim-bullseye AS base

RUN apt-get update && \
    apt-get install build-essential -y

RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf # Temporarily lower security to workaround opentest certs with SHA1 signatures

RUN mkdir -p /usr/src/app/mhs/spineroutelookup

COPY mhs/spineroutelookup/Pipfile /usr/src/app
COPY mhs/spineroutelookup/Pipfile.lock /usr/src/app

RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/spineroutelookup/ /usr/src/app/mhs/spineroutelookup

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/common"

WORKDIR /usr/src/app/mhs/spineroutelookup

RUN pipenv --python 3.7
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 80

ENTRYPOINT pipenv run start
