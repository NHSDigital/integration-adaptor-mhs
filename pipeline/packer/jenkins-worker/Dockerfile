FROM jenkins/jnlp-slave:4.13.3-1

# Need to be root to install packages
USER root

# Fix local cache
RUN rm -rf /var/lib/apt/lists/* && apt update

# Install Packer
RUN apt-get install wget unzip && \
        wget -O packer.zip https://releases.hashicorp.com/packer/1.4.2/packer_1.4.2_linux_amd64.zip && \
        unzip packer.zip -d /usr/bin/ && \
        rm packer.zip

# Install Terraform
RUN wget -O terraform.zip https://releases.hashicorp.com/terraform/0.12.31/terraform_0.12.31_linux_amd64.zip && \
        unzip terraform.zip -d /usr/bin/ && \
        rm terraform.zip

# Install Python 3.9
RUN apt-get update && apt-get install -y build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev libgdbm-dev libc6-dev libbz2-dev uuid-dev zlib1g-dev libffi-dev swig pkg-config && \
        wget -O python.tgz https://www.python.org/ftp/python/3.9.19/Python-3.9.19.tgz && \
        tar -xf python.tgz && rm python.tgz && \
        cd Python-3.9.19 && \
        ./configure && make && make install && \
        cd .. && rm -rf Python-3.9.19

# Install pipenv
RUN pip3 install pipenv

# Install sonar scanner
RUN wget -O sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.0.0.1744-linux.zip && \
        unzip sonar-scanner.zip -d /opt/sonar-scanner/ && \
        chmod +x /opt/sonar-scanner/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner && \
        ln -s /opt/sonar-scanner/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner /usr/bin/sonar-scanner && \
        rm sonar-scanner.zip

# Install Docker
# These commands are based on https://docs.docker.com/install/linux/docker-ce/debian/ and https://github.com/ninech/jnlp-slave-with-docker
# This relies on docker.sock being exposed to the Jenkins slave
RUN apt-get update && \
        apt-get install -qq -y --no-install-recommends \
        apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
        apt-key fingerprint 0EBFCD88 && \
        add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
        apt-get update && \
        apt-get install -qq -y --no-install-recommends docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
        echo 'docker compose --compatibility "$@"' > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

# Install curl and libSSL, so Tornado can use the CURL HTTP client.
RUN apt-get update && apt-get install -y libcurl4-openssl-dev libssl-dev

# Install awscli
ENV AWS_CLI_VERSION="2.17.27"
RUN curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip -o awscli-bundle.zip && \
        unzip awscli-bundle.zip && \
        ./aws/install && \
        rm -rf aws*

# Cleanup

RUN apt-get clean

# Leave as root to allow for running docker builds

ENTRYPOINT ["jenkins-slave"]