MHS Containers
==============
Scripts have been provided for each release of the adaptor and are stored in the MHS Adaptor Git repository. There are shell scripts that are useful for examples on how to structure your requests to the MHS Adaptor.

Quickstart
---------------
To get running make sure you have an OpenTesst environment setup.

Clone the MHS Adaptor Git repository:
```bash
$ git clone https://github.com/nhsconnect/integration-adaptor-mhs
```

Navigate to the test-scripts folder:
```bash
$ cd integration-adaptor-mhs
```

Set up your OpenTest details using export-env-vars.sh.example as a template:
```bash
$ cp export-env-vars.sh.example export-env-vars.sh
```

Start the containers:
```bash
$ cd 0.0.2
$ ./run.sh
```

You can verify that all the containers defined in the docker-compose.yml file in that folder are running:
```bash
$ docker-compose ps
```

Start testing!

> There are shell scripts in each of the release version folders that provide examples on how to structure your tests.

To stop the containers:
```bash
$ docker-compose down
```


