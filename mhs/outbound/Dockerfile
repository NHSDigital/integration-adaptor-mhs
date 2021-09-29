ARG BASE_IMAGE_TAG=latest
FROM nhsdev/nia-mhs-outbound-base:$BASE_IMAGE_TAG

RUN mkdir -p /usr/src/app/mhs/outbound

COPY mhs/outbound/Pipfile /usr/src/app
COPY mhs/outbound/Pipfile.lock /usr/src/app

RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/outbound/ /usr/src/app/mhs/outbound

WORKDIR /usr/src/app/mhs/outbound

RUN pipenv --python 3.7
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 80

ENTRYPOINT pipenv run start
