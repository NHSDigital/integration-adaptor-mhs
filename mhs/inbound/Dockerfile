ARG BASE_IMAGE_TAG=latest
FROM nhsdev/nia-mhs-inbound-base:$BASE_IMAGE_TAG

RUN mkdir -p /usr/src/app/mhs/inbound

RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/inbound/ /usr/src/app/mhs/inbound

WORKDIR /usr/src/app/mhs/inbound
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/common"

RUN pipenv --python 3.7
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --dev --deploy --ignore-pipfile

EXPOSE 443 80

ENTRYPOINT pipenv run start
