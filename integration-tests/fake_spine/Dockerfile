FROM python:3.7-slim-bullseye

# Install necessary packages
RUN apt-get update && apt-get install -y build-essential git

# Create necessary directories
RUN mkdir -p /usr/src/app/mhs/fakespine

# Install pipenv
RUN pip install pipenv

# Copy necessary files
COPY common/ /usr/src/app/common/
COPY integration-tests/fake_spine/ /usr/src/app/mhs/fakespine
WORKDIR /usr/src/app/mhs/fakespine
COPY integration-tests/fake_spine/Pipfile /usr/src/app
COPY integration-tests/fake_spine/Pipfile.lock /usr/src/app

# Set up pipenv environment
RUN pipenv --python 3.7
RUN pipenv run uninstall_setuptools
RUN pipenv run install_setuptools
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application
COPY . .

# Expose ports
EXPOSE 80 443

# Set entrypoint
ENTRYPOINT ["pipenv", "run", "start", "--logging=DEBUG"]
