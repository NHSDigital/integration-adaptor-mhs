FROM python:3.7-slim-bullseye as base

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev swig pkg-config

# Replace security level 2 with security level 1.
# Temporarily lower security to workaround opentest certs with SHA1 signatures.
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/' /etc/ssl/openssl.cnf
