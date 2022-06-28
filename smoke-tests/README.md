# Smoke Tests

### How to run the tests

The smoke tests verify the services and resources required by the MHS Adaptor are running.

To run the smoke tests:

- Ensure JDK 17 is installed
- Start the adaptors services and resources using an appropriate environment configuration.  
- Navigate to the `smoke-tests` directory
- Run the helper script `./run-smoke-tests.sh <vars.sh>`, where `<vars.sh>` 
is a configuration shell script 

`<vars.sh>` should export the environment variables that were used to configure the adaptor.
An `example-vars.sh`script is included for reference [here](./example-vars.sh), 
this contains the environment variables the smoke tests require.

### Docker override script

The smoke tests require the healthcheck endpoint is available for the Inbound Service. 
As this is not exposed via the base docker-compose.yml script an override script has been provided.

So, for example, the adaptor can be run using: 

```
docker-compose -f docker-compose.yml -f docker-compose.smoke.test.override.yml up
```

And this will expose the healthcheck endpoint on the port specified by the 
`MHS_INBOUND_HEALTHCHECK_SERVER_PORT` environment variable.