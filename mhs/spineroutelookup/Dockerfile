ARG BASE_IMAGE_TAG=latest
FROM nhsdev/nia-sds-base:$BASE_IMAGE_TAG

RUN mkdir -p /usr/src/app/mhs/spineroutelookup

# Install dependencies for adding a Python 3.8
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.8 python3.8-venv python3.8-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Install pip and pipenv for Python 3.8
RUN apt-get install -y python3-pip && \
    python3.8 -m pip install --upgrade pip
RUN pip install pipenv

COPY mhs/spineroutelookup/Pipfile /usr/src/app
COPY mhs/spineroutelookup/Pipfile.lock /usr/src/app
COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/spineroutelookup/ /usr/src/app/mhs/spineroutelookup

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/mhs/common"
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/common"

WORKDIR /usr/src/app/mhs/spineroutelookup

RUN pipenv --python 3.8
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 80

ENTRYPOINT pipenv run start
