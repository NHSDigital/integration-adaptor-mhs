
# Quick reference
- Maintained by: NHS Digital
- Where to get help: https://github.com/nhsconnect/integration-adaptor-mhs
- Where to file issues: https://github.com/nhsconnect/integration-adaptor-mhs/issues

# What is the MHS Adaptor?
A pre-assured implementation of a Message Handling Service (MHS), that encapsulates the details of Spine messaging and provides a simple interface to allow HL7 messages to be sent to the NHS spine MHS.

# How to use this image
## Pre-requisites
To get running make sure you have an OpenTest environment setup.

## Clone the repository
```bash
$ git clone https://github.com/nhsconnect/integration-adaptor-mhs
```

## Find the test scripts folder
```bash
$ cd integration-adaptor-mhs
```

## Setup your OpenTest details
Set up your OpenTest details using export-env-vars.sh.example as a template:
```bash
$ cp export-env-vars.sh.example export-env-vars.sh
```
Populate the variables in this file with the details provided when you signed up for OpenTest.

## Start it up
```bash
$ cd 0.0.2
$ ./run.sh
```

You can verify that all the containers defined in the docker-compose.yml file in that folder are running:
```bash
$ docker-compose ps
```

## Start testing!

There are shell scripts in each of the release version folders that provide examples on how to structure your tests.

## Stopping the adaptor
```bash
$ docker-compose down
```