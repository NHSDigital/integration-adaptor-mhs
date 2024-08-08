ARG BASE_IMAGE_TAG=latest
FROM nhsdev/nia-sds-base:$BASE_IMAGE_TAG

RUN mkdir -p /usr/src/app/mhs/spineroutelookup

# Install dependencies for adding Python 3.8
RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget  \
    curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
RUN wget https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tgz && \
    tar -xvzf Python-3.8.17.tgz && \
    cd Python-3.8.17 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -s /usr/local/bin/python3.8 /usr/bin/python3.8

# Set Python 3.8 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 1

# Install pip for Python 3.8
RUN apt-get install -y python3-pip && \
    python3.8 -m pip install --upgrade pip

# Install pipenv
RUN pip install pipenv

COPY mhs/spineroutelookup/Pipfile /usr/src/app
COPY mhs/spineroutelookup/Pipfile.lock /usr/src/app

RUN pip install pipenv

COPY common/ /usr/src/app/common/
COPY mhs/common/ /usr/src/app/mhs/common/
COPY mhs/spineroutelookup/ /usr/src/app/mhs/spineroutelookup

ENV PYTHONPATH="/usr/src/app/mhs/common:/usr/src/app/common"

WORKDIR /usr/src/app/mhs/spineroutelookup

RUN pipenv --python 3.8
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 80

ENTRYPOINT ["pipenv", "run", "start"]
