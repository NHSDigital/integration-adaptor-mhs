# Operating the MHS Adaptor

This following is a guide to operational considerations where the MHS Adaptor is deployed within your infrastructure

## Environment Variables

MHS takes a number of environment variables when it is run. Some of the variables are environment specific (OpenTest, PTL and if necessary the Fakespine).  You can find more information on environment config values in the [OpenTest](https://digital.nhs.uk/services/spine/open-access-test-environment-for-spine-opentest) and [Path To Live](https://digital.nhs.uk/services/path-to-live-environments) portal pages.

The list of environment variables are:
* `MHS_LOG_LEVEL` This is required to be set to one of: `INFO`, `WARNING`, `ERROR` or `CRITICAL`, where `INFO` displays
the most logs and `CRITICAL` displays the least. Note: Setting this value to one of the more detailed 'standard' Python
log levels (such as `DEBUG` or `NOTSET`) may result in the libraries used by this application logging details that
contain sensitive information such as the content of messages being sent.
* `MHS_SECRET_PARTY_KEY` (inbound & outbound only) The party key associated with your MHS.
* `MHS_SECRET_CLIENT_CERT` Your endpoint certificate
* `MHS_SECRET_CLIENT_KEY` Your endpoint private key
* `MHS_SECRET_CA_CERTS` Should include the following in this order: endpoint issuing subCA certificate, root CA Certificate.
* `MHS_STATE_TABLE_NAME` (inbound & outbound only) The name of the DB table used to store MHS state.
* `MHS_SYNC_ASYNC_STATE_TABLE_NAME` (inbound & outbound only) The table name used to store sync async responses
* `MHS_STATE_STORE_MAX_RETRIES'` (inbound & outbound only) The max number of retries when attempting to interact with either the work description or sync-async store. Defaults to `3`
* `MHS_OUTBOUND_TRANSMISSION_MAX_RETRIES` (outbound only) This is the maximum number of retries for outbound requests. If no value is given a default of `3` is used.
* `MHS_OUTBOUND_TRANSMISSION_RETRY_DELAY` (outbound only) The delay between retries of outbound requests in milliseconds. If no value is given, a default of `100` is used.
* `MHS_OUTBOUND_HTTP_PROXY` (outbound only) An optional http(s) proxy to route downstream requests via. Note that the proxy must passthrough https requests transparently.
* `MHS_OUTBOUND_HTTP_PROXY_PORT` (outbound only) The http(s) proxy port to use. Ignored if `MHS_OUTBOUND_HTTP_PROXY` is not provided. Defaults to `3128`.
* `MHS_OUTBOUND_VALIDATE_CERTIFICATE` (outbound only) Verification of the server certificate received when making a connection to the spine MHS.
* `MHS_INBOUND_QUEUE_BROKERS` (inbound only) The url(s) of the amqp inbound queue broker(s). e.g. `amqps://example.com:port`. Note that if the amqp connection being used is a secured connection (which it should be in production), then the url should start with `amqps://` and not `amqp+ssl://`. This URL should not include the queue name. Can be a coma-separated list or urls for HA
* `MHS_INBOUND_QUEUE_NAME` The name of the queue on the broker identified by `MHS_INBOUND_QUEUE_BROKERS` to place inbound messages on. e.g `queue-name`
* `MHS_INBOUND_QUEUE_MESSAGE_TTL_IN_SECONDS` Defines Time-To-Live of inbound queue messages
* `MHS_SECRET_INBOUND_QUEUE_USERNAME` (inbound only) The username to use when connecting to the amqp inbound queue.
* `MHS_SECRET_INBOUND_QUEUE_PASSWORD` (inbound only) The password to use when connecting to the amqp inbound queue.
* `MHS_INBOUND_QUEUE_MAX_RETRIES` (inbound only) The max number of times to retry putting a message onto the amqp inbound queue. Defaults to `3`.
* `MHS_INBOUND_QUEUE_RETRY_DELAY` (inbound only) The delay in milliseconds between retrying putting a message onto the amqp inbound queue. Defaults to `100`ms.
* `MHS_SYNC_ASYNC_STORE_MAX_RETRIES'` (inbound only) The max number of retries when attempting to add a message to the sync-async store. Defaults to `3`
* `MHS_SYNC_ASYNC_STORE_RETRY_DELAY` (inbound only) The delay in milliseconds between retrying placing a message on the sysnc-async store. Defaults to `100`ms
* `MHS_RESYNC_RETRIES` (outbound only) The total number of attempts made to the sync-async store during resynchronisation, defaults to `20`
* `MHS_RESYNC_INTERVAL` (outbound only) The time in between polls of the sync-async store, the interval is in seconds and defaults to `1`
* `MHS_SPINE_ROUTE_LOOKUP_URL` (outbound only) The URL of the Spine route lookup service. E.g `https://example.com`. This URL should not contain path or query parameter parts.
* `MHS_SPINE_ORG_CODE` (outbound only) The organisation code for the Spine instance that your MHS is communicating with. E.g `YES`
* `MHS_FORWARD_RELIABLE_ENDPOINT_URL` (outbound only) The URL to communicate with Spine for Forward Reliable messaging
* `MHS_RESYNC_INITIAL_DELAY` (Outbound service only) The initial delay (in seconds) before making the first poll to the sync-async
    store after the outbound service receives an acknowledgement from Spine
* `MHS_SPINE_REQUEST_MAX_SIZE` (outbound service only) The maximum size (in bytes) that request bodies sent to Spine
are allowed to be. This should be set minus any HTTP headers and other content in the HTTP packets sent to Spine.
e.g. Setting this to ~400 bytes less than the maximum request body size should be roughly the correct value
(calculating this value accurately is pretty much impossible as one of the HTTP headers is the Content-Length header
which varies depending on the request body size).
* `MHS_DB_ENDPOINT_URL` The URL for the adaptors DB
* `MHS_CLOUD_REGION` Cloud region that the adaptor has/will be been deployed to
* `MHS_PERSISTENCE_ADAPTOR` Used to determine the type of persistence adaptor to implement (dynamodb/mongodb)  
* `MHS_LOG_FORMAT` #[%(asctime)sZ] | %(levelname)s | %(process)d | %(interaction_id)s | %(message_id)s | %(correlation_id)s | (inbound_message_id)s | %(name)s | %(message)s"
* `MHS_INBOUND_USE_SSL` Boolean for the use of SSL. Only for testing purpose to facilitate local development debugging
* `MHS_INBOUND_SERVER_PORT` Define a specific port when connecting to the Inbound service. Defaults to '443'
* `MHS_INBOUND_HEALTHCHECK_SERVER_PORT` Define a specific port when connecting to the Inbound Healthcheck service. Defaults to '8082'
* `MHS_OUTBOUND_SERVER_PORT` Define a specific port when connecting to the Outbound service. Defaults to '80'
* `MHS_OUTBOUND_ROUTING_LOOKUP_METHOD` Define which lookup method to use for routing and reliability. One of `SPINE_ROUTE_LOOKUP` or `SDS_API`

Following variables are required if `MHS_OUTBOUND_ROUTING_LOOKUP_METHOD` is set to `SPINE_ROUTE_LOOKUP`
* `MHS_LAZY_LDAP` use lazy connection from spine route lookup component to SPINE LDAP service
* `MHS_SECRET_SPINE_ROUTE_LOOKUP_CLIENT_CERT` (outbound only) Optional. The client certificate to present when making HTTPS connections to the Spine Route Lookup service. If not specified, no client certificate will be presented.
* `MHS_SECRET_SPINE_ROUTE_LOOKUP_CLIENT_KEY` (outbound only) Optional. The private key for the client certificate to present when making HTTPS connections to the Spine Route Lookup service. Must be specified if `MHS_SPINE_ROUTE_LOOKUP_CLIENT_CERT` is provided.
* `MHS_SECRET_SPINE_ROUTE_LOOKUP_CA_CERTS` (outbound only) Optional. The CA certificates used to validate the certificate presented by the Spine Route Lookup service. Should include the following in this order: endpoint issuing subCA certificate, root CA Certificate. If not specified, the system defaults will be used.
* `MHS_SPINE_ROUTE_LOOKUP_HTTP_PROXY` (outbound only) An optional http(s) proxy to route requests to the Spine Route Lookup service via. Note that the proxy must pass through https requests transparently.
* `MHS_SPINE_ROUTE_LOOKUP_HTTP_PROXY_PORT` (outbound only) The http(s) proxy port to use for the Spine Route Lookup service proxy. Ignored if `MHS_SPINE_ROUTE_LOOKUP_HTTP_PROXY` is not provided. Defaults to `3128`.
* `MHS_SDS_URL` (Spine Route Lookup service only) The URL to communicate with SDS on. e.g. `ldaps://example.com`
* `MHS_SDS_SEARCH_BASE` (Spine Route Lookup service only) The LDAP location to use as the base of SDS searches, e.g. `ou=services,o=nhs`. This value is specific to the SDS instance you configure your MHS to communicate with and should not contain whitespace.
* `MHS_DISABLE_SDS_TLS` (Spine Route Lookup service only) An optional flag that can be set to disable TLS for SDS
connections. *Must* be set to exactly `True` for TLS to be disabled.
* `MHS_SDS_CACHE_EXPIRY_TIME` (Spine Route Lookup service only). An optional value that specifies the time (in seconds)
that a value should be held in the SDS cache. Defaults to `900` (fifteen minutes)
* `MHS_SDS_REDIS_CACHE_HOST` (Spine Route Lookup service only). The Redis host to use when caching SDS information
retrieved from SDS.
* `MHS_SDS_REDIS_CACHE_PORT` (Spine Route Lookup service only). An optional value that specified the port to use when
connecting to the Redis host specified by `MHS_SDS_REDIS_CACHE_HOST`. Defaults to `6379`.
* `MHS_SDS_REDIS_DISABLE_TLS` (Spine Route Lookup service only) An optional flag that can be set to disable TLS for
connections to the Redis cache used by the Spine Route Lookup service. *Must* be set to exactly `True` for TLS to be
disabled.
* `MHS_SPINE_ROUTE_LOOKUP_SERVER_PORT`Define a specific port when connecting to the Spine Route Lookup service. Defaults to '80'
* `MHS_LDAP_CONNECTION_RETRIES` Retry attempt value when attempting LDAP connection 
* `MHS_LDAP_CONNECTION_TIMEOUT_IN_SECONDS` Timeout value when attempting LDAP connection

Following variables are required if `MHS_OUTBOUND_ROUTING_LOOKUP_METHOD` is set to `SDS_API`
* `MHS_SDS_API_URL` URL to SDS API. e.g. `https://sandbox.api.service.nhs.uk/spine-directory/FHIR/R4`
* `MHS_SDS_API_KEY` api key to authenticate with when sending requests to SDS API

Note that if you are using Opentest, you should use the credentials you were given when you got access to set `MHS_SECRET_PARTY_KEY`, `MHS_SECRET_CLIENT_CERT`, `MHS_SECRET_CLIENT_KEY` and `MHS_SECRET_CA_CERTS`.


## Log consumption
The MHS Adaptor emit logs and audit records on standard I/O streams which are captured by the Docker containers they are hosted within. 
Whichever Docker container orchestration technology is used, these log streams can be captured and/or forwarded to an appropriate log indexing 
service for consumption, storage and subsequent query.

The [AWS exemplar](README.md#aws-exemplar) deployment of the MHS Adaptor makes use of the ECS Fargate service and the logs are captured into the 
CloudWatch Logs service. Additionally logs produced by other cloud infrastructure such as load balancers are also captured into the CloudWatch Logs service, 
so that logs are comprehensively captured across the whole solution allowing for joined up querying.

## Choice of tooling
However the MHS Adaptor is deployed, logs should be forwarded to a suitable log indexing service. Suggested examples are:

- AWS CloudWatch Logs is a common choice for log indexing for AWS deployments
    - Logs indexed in CloudWatch Logs can be queried and analysed using the AWS tool CloudWatch Logs Insights.
    - If Splunk is your organisation's preferred log analysis tool, there are a number of methods for integrating Splunk with CloudWatch Logs including the Splunk AWS Add-on, the use of Kinesis or Lambdas to forward logs, or by querying the CloudWatch Logs Insights API.
    - Other solutions such as DataDog, New Relic, Grafana, Elastic Stack, or Prometheus offer similar tools for monitoring, calculating metrics, graphing and creating dashboards and alerting. These tools all have modes of integration with CloudWatch Logs.
- In Azure, Azure Monitor is a common choice for log indexing for Azure deployments
    - Azure Monitor comprises of a suite of services for log and metric capture and storage, alerting, analysis, visualisation and dashboard creation and the creation of insights.
    - Azure Monitor also has APIs for integration of other tools.
    - It has features designed for specific patterns of cloud deployment, including capabilities tailored to Containers hosted in Azure Kubernetes Service.
    - Microsoft's Power BI tool can be configured to automatically import data from Azure Monitor for more business-centric analytics.
    - Other solutions such as DataDog, AppDynamics, Elastic Stack, Grafana, NewRelic, SolarWinds, Splunk and Sumo Logic can be integrated through Azure Monitor Export APIs.

Key requirements that should be prioritised when choosing a service for log indexing, storage, query and analytics are:

- Ability to parse key-value pairs in log lines and infer/interpret the data types of values
- Ability to build complex queries which filter and/or aggregate values using those key-value pairs
- Ability to index and present log records in time series order with timestamp values interpreted to the full accuracy present in the logs (e.g. millisecond)
- Ability to tie together multiple logs for flow analysis across multiple components using a common correlation ID
- Facilities to calculate aggregate metrics, such as moving averages or totals, across a defined set of log messages.
- Facilities for graphing, dashboard creation and analytical interaction with the presented data
- Ability to implement a log retention policy, including log rotation, and full deletion of "rolled" logs
- Secure storage and handling of log data
- Role based access control including the ability to differentiate groups of logs for more strict permissions and restrict access to audit logs to a specific group of users
- Backup to cold storage
- Ability to raise alerts that notify subscribed users immediately upon certain events happening such as presence of specific types of log, or breach of thresholds.
- Ability to highlight and alert on the absence of log data from an expected component, indicating a component silently failing.

## MHS Adaptor resource allocation
The recommended memory for the PS Adaptor Translator is 4 GB. Also, it should be run on (at least) two CPUs for better performance.

### Audit consumption

Audit logs are emitted through the same channel as other log messages, via the standard I/O streams captured and forwarded by Docker. Audit log messages have a log level of AUDIT which is used to differentiate them from other logs. Due to the potential sensitivity of the data held in AUDIT logs and the need to ensure that AUDIT logs have stronger controls around them to prevent the possibility of tampering, it is strongly advised that the log indexing tooling chosen should be configured to filter AUDIT logs out of the main log bucket and divert them into their own audit log bucket, which can be stored and controlled separately.

## Log Format

First few logs don't follow the pattern as they are written before logger initialization. Those are minor read configuration logs. Pattern: 

```text
[%(asctime)sZ] | %(levelname)s | %(process)d | %(interaction_id)s | %(message_id)s | %(correlation_id)s | %(inbound_message_id)s | %(name)s | %(message)s
```

Log messages produced by the MHS Adaptor are in human readable form and important data is included within the log message as key=value pairs so that they can be parsed 
and used for searching, filtering, agregation, graphing etc. Few first logs don't follow the pattern as they are written before logger initialization. 
Those are minor read-config logs.

```text
2020-03-26T10:31:52.118165Z | AUDIT | 40186 | QUPC_IN160101UK05 | 4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703 | 1 |  | outbound.mhs_common.workflow.asynchronous_express | WorkflowName=async-express outbound workflow invoked.
```
The pattern is as follows (mind that inbound_message_id is missing in the example above):
```text
"[%(asctime)sZ] | %(levelname)s | %(process)d | %(interaction_id)s | %(message_id)s | %(correlation_id)s | %(inbound_message_id)s | %(name)s | %(message)s"
```

- The start of the log line included a datetime-stamp in ISO8601 timestamp format and always in UTC timezone.

- The above example does not contain an `inbound_message_id` as this log is from outbound. Only logs from inbound that are not unsolicited will contain this id. 

- The end of the log line contains some log messages:

| Common Key | Purpose |
| ---------- |:------- |
| `Time` | Datetime-stamp in ISO8601 timestamp format and always in UTC timezone. |
| `LogLevel` | The level at which the log line was raised. |
| `pid` | Process ID, identifies the running instance of a component that produced the log message. |
| `InteractionId` | ID of interaction that you want to invoke. Each interaction has an associated workflow (sync, async express, async reliable and forward reliable)) and a corresponding syn-async flag.
| `MessageId` | A unique ID which is generated at the very start of a workflow if not already assigned. |
| `CorrelationId` | A unique ID which is generated at the very start of a workflow and is used throughout all log messages related to that work, such that all the logs in the chain can be tied together for a single work item. CorrelationId can be passed into the MHS components from the supplier's calling client to allow for the CorrelationId to also tie the workflow together with the client system. |
| `RefToMessageId` | A unique ID which is generated at the very start of a workflow as the MessageID if not already assigned. When a message is returned from spine originating from outbound, this UUID will be assigned as the RefToMessageId in spine. Incoming inbound messages will have a new MessageId, and RefToMessageId that refer to original message_id of outbound message. Used to find if message id exists in state database to determine if message is unsolicited or not. |
| `LoggerName` | Identifies the sub-component within the solution which produced the logs.  It's a dot-separated name where the first part is the component that produced the log. |
| `Log Message` | Information that is logged. |

## Log Level
The logs produced by the MHS Adaptor application components have one of the following log levels, the following table describes the semantics of each log level:

| Log Level | Description |
| --------- | ----------- |
| `INFO` | General information messages and confirmation that things are working as expected. Allows for tracking of work following through the system, points-of-interest, and where uncommon logical flows have been invoked. |
| `AUDIT` | Specific logging of auditable events in the business process. See section below for further coverage of Audit logs. |
| `WARNING` | Indication that something unexpected has happened but is being handled, such as processing of an invalid message, invocation of error handling logic which is not expected to be executed through the specified processing. It can also be used to raise a warning about a potential future problem, such as levels or disk space or memory reaching a threshold. When using WARNING, the software is still working as expected, higher log levels are used when this is not the case. |
| `ERROR` | Due to a more serious and unhandlable error, the software has not been able to perform some function. This may result in a request erroring or an item of work being unable to be processed further without further intervention and remediation. <br/><br/> The application should be able to recover from an ERROR scenario using its error handling logic and continue normal operations, processing other requests/messages without deterioration, if it cannot then a higher log level will be used.|
| `CRITICAL` | Indicates a problem, which may still be handled by error handling logic, but which is likely to compromise the on-going operation of the component. This is also used where error handling logic has failed and final logs are being produced before the process/service dies. |

The MHS Adaptor components have specifically chosen INFO as the lowest log level, rather than DEBUG. The principle here is that all information logged is potentially useful for diagnosing live issues, and so should be available in Production. It is not recommended to enable DEBUG level logging in production, so it is important that the lowest level of logs emitted from the MHS Adaptor components to facilitate diagnostics is INFO.

> [!WARNING]
> The third party libraries used by the MHS Adaptor will likely emit logs at DEBUG if this level is
> configured on, however suppliers should be aware that DEBUG level logs from components involved in
> I/O are highly likely to include the entire message payload which in the context of the MHS Adaptor
> is likely to contain Patient Identifying Information and other sensitive data.
> As such it is strongly recommended that DEBUG log level never be configured on in Production
> environments, to ensure that real patient data does not leak into log files.
> 
> The performance of the Inbound and Outbound adaptors are adversely affected when DEBUG mode is
> enabled when using AWS ECS, CloudWatch and the aws-logs driver.
> When a large (~5MB) request body is printed out to the console in DEBUG, this data can take several
> seconds to be ingested by CloudWatch, during which the respective adaptor is unresponsive.
> During a large GP2GP transfer where multiple incoming or outgoing requests are made at once this
> unresponsiveness can cause spine requests to fail.
> 
> In a non-production environment, one workaround for the AWS CloudWatch issue is to use the
> [non-blocking mode][cloudwatch-config-options].


[cloudwatch-config-options]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html?icmpid=docs_ecs_hp-task-definition#create_awslogs_logdriver_options

### Audit Messages

Every outbound and inbound message which passes through the MHS Adaptor produces an audit log message. Following is an example of the format:

```text
20-03-26T10:31:52.500735Z | AUDIT | 40186 | QUPC_IN160101UK05 | 4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703 | 1 |  | outbound.mhs_common.workflow.common_asynchronous | WorkflowName=async-express outbound workflow invoked. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_ACKD received.
```
Audit messages are produced with the log level of AUDIT.

`Acknowledgement` indicates the status of the ACK response received from Spine.

`RequestSentTime` is the time the outgoing message was sent to Spine by the MHS Adaptor.

`AcknowledgementReceivedTime` is the time the ACK response was received from Spine by the MHS Adaptor.

See above for details of `Time`, `LogLevel`, `pid`, `InteractionId`, `MessageId`, `CorrelationID`, `RefToMessageId`, `Loggername` and `Log Message`.

### Workflow processes

Log examples of the four different workflow processes, Asynchronous Express, Asynchronous Reliable, Synchronous asynchronous and Synchronous. 

It is known that libraries used by this application sometimes log out clinical patient data at DEBUG level. The log level provided MUST NOT be used in a production environment. 

#### Asynchronous Express 

| No. | Log Line |  Description | 
| --- | -------- | -----------  | 
| 1 | `Entered async express workflow to handle outbound message` | Started Outbound async-express workflow started to handle incoming message |
| 2 | `Attempting to publish work description key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | Attempts to publish the local state of the work description to the state store for new message to outbound |
| 3 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 4 | `No previous version found, continuing attempt to publish new version` | Checks versions to avoid collisions. No remote version found, continues attempt to publish new remote version with current timestamp |
| 5 | `Successfully updated work description to state store for key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | State: VERSION: `1`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_RECEIVED` |
| 6 | `Looking up endpoint details for ods code: ods_code=YES.` | Confirmation from spine route lookup, ods code set to `yes` to communicate to spine |
| 7 | `Looking up endpoint details for service_id=urn:nhs:names:services:psisquery:QUPC_IN160101UK05.` | Request made to retrieve routing details from spine route lookup |
| 8 | `Retrieved endpoint details for details="{'service_id': 'urn:nhs:names:services:psisquery:QUPC_IN160101UK05', 'url': 'https://192.168.128.11/reliablemessaging/queryrequest', 'party_key': 'YES-0000806', 'cpa_id': 'S20003A000304', 'to_asid': '227319907548'}"` | Confirmation endpoint details successfully retrieved from spine route lookup |
| 9 | `Message serialised successfully` | Serialize outbound message with routing information and previous incoming message data such as `message_id`, `correlation_id`, `interaction_details`, `payload`, `wdo`,`to_party_key`, `cpa_id` |
| 10 | `Attempting to publish work description key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | Attempts to publish the local state of the work description to the state store to update state database with message state spine route lookup workflow complete |
| 11 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 12 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 13 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, increments local version number |
| 14 | `Successfully updated work description to state store for key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | State: VERSION: `2`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_PREPARED` |
| 15 | `About to make outbound request` | Starting process to send message request from Outbound to Spine |
| 16 | `WorkflowName=async-express outbound workflow invoked. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_ACKD received.` | Message successfully sent to spine from outbound and spine returned acknowledgement |
| 17 | `Attempting to publish work description key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | Attempts to publish the local state of the work description to the state store to update message state with this information received spine |
| 18 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 19 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 20 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 21 | `Successfully updated work description to state store for key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | State: VERSION: `3`, INBOUND_STATUS: `INBOUND_RESPONSE_RECEIVED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_PREPARED` |
| 22 | `Entered WorkflowName=async-express workflow to handle inbound message` | Starting Inbound async-express workflow to handle message from spine |
| 23 | `Attempting to publish work description key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | Attempting to publish key to state database |
| 24 | `Retrieving latest work description to check version` | Query state database to check if version exists |
| 25 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 26 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 27 | `Successfully updated work description to state store for key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | State: VERSION: `4`, INBOUND_STATUS: `INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED`, OUTBOUND_STATUS: `SYNC_RESPONSE_SUCCESSFUL` | 
| 28 | `Placed message onto inbound queue successfully` | Confirmation message added to inbound queue |
| 29 | `Attempting to publish work description key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | Attempting to publish key to state database |
| 30 | `Retrieving latest work description to check version` | Query state database to check if version exists |
| 31 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 32 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 33 | `Successfully updated work description to state store for key=4DE4BBB7-F1DE-48BD-8824-E8FFCE4FC703` | State: VERSION: `5`, INBOUND_STATUS: `INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 34 | `WorkflowName=async-express inbound workflow completed. Message placed on queue, returning Acknowledgement=MessageStatus.INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED to spine` | Confirmation of inbound workflow completed. |

#### Asynchronous Reliable

| No. | Log Line |  Description | 
| --- | -------- | -----------  | 
| 1 | `Entered async reliable workflow to handle outbound message` | Started Outbound async reliable workflow started to handle incoming message |
| 2 | `Attempting to publish work description key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | Attempts to publish the local state of the work description to the state store for new message to outbound |
| 3 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 4 | `No previous version found, continuing attempt to publish new version` | Checks versions to avoid collisions. No remote version found, continues attempt to publish new remote version with current timestamp |
| 5 | `Successfully updated work description to state store for key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | State: VERSION: `1`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_RECEIVED` |
| 6 | `Looking up endpoint details for ods code: ods_code=YES.` | Confirmation from spine route lookup, ods code set to `yes` to communicate to spine |
| 7 | `Looking up endpoint details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05.` | Request made to routing details from spine route lookup |
| 8 | `Retrieved endpoint details for details="{'service_id': 'urn:nhs:names:services:psis:REPC_IN150016UK05', 'url': 'https://192.168.128.11/reliablemessaging/reliablerequest', 'party_key': 'YES-0000806', 'cpa_id': 'S20001A000182', 'to_asid': '227319907548'}"` | Confirmation endpoint successfully retrieved routing details from spine route lookup |
| 9 | `Looking up reliability details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05.` | Request made to reliability details from spine route lookup |
| 10 | `Retrieved reliability details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05. reliability_details="{'nhsMHSSyncReplyMode': 'MSHSignalsOnly', 'nhsMHSRetryInterval': 'PT1M', 'nhsMHSRetries': '2', 'nhsMHSPersistDuration': 'PT5M', 'nhsMHSDuplicateElimination': 'always', 'nhsMHSAckRequested': 'always'}"` | Confirmation endpoint successfully reliability details from spine route lookup |
| 11 | `Message serialised successfully` | Serialize outbound message with routing information and previous incoming message data such as `message_id`, `correlation_id`, `interaction_details`, `payload`, `wdo`,`to_party_key`, `cpa_id` |
| 12 | `Attempting to publish work description key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | Attempts to publish the local state of the work description to the state store to update message state that spine route lookup workflow complete |
| 13 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 14 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 15 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, increments local version number |
| 16 | `Successfully updated work description to state store for key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | State: VERSION: `2`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_PREPARED` |
| 17 | `About to make outbound request` | Starting process to send message request from Outbound to Spine |
| 18 | `WorkflowName=async-reliable outbound workflow invoked. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_ACKD received.` | Message successfully sent to spine from outbound and spine returned acknowledgement |
| 19 | `Attempting to publish work description key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | Attempts to publish the local state of the work description to the state store to update message state from this information received spine |
| 20 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 21 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 22 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 23 | `Successfully updated work description to state store for key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | State: VERSION: `3`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 24 | `Entered WorkflowName=async-reliable workflow to handle inbound message` | Starting Inbound async-reliable workflow to handle message from spine |
| 25 | `Attempting to publish work description key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | Attempting to publish key to state database |
| 26 | `Retrieving latest work description to check version` | Query state database to check if version exists |
| 27 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 28 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 29 | `Successfully updated work description to state store for key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | State: VERSION: `4`, INBOUND_STATUS: `INBOUND_RESPONSE_RECEIVED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 30 | `Placed message onto inbound queue successfully` | Confirmation message added to inbound queue |
| 31 | `Attempting to publish work description key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | Attempting to publish key to state database |
| 32 | `Retrieving latest work description to check version` | Query state database to check if version exists |
| 33 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 34 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 35 | `Successfully updated work description to state store for key=30446459-2A2C-4B56-8C5D-A89B3B3377DF` | State: VERSION: `5`, INBOUND_STATUS: `INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 36 | `WorkflowName=async-reliable inbound workflow completed. Message placed on queue, returning Acknowledgement=MessageStatus.INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED to spine` | Confirmation of inbound workflow completed. |

#### Synchronous asynchronous

| No. | Log Line |  Description | 
| --- | -------- | -----------  | 
| 1 | `Entered sync-async workflow to handle outbound message` | Started Outbound sync-async workflow started to handle incoming message, flag telling outbound to wait for async response |
| 2 | `Entered async reliable workflow to handle outbound message` | Started Outbound async reliable workflow started to handle sync-async message |
| 3 | `Looking up endpoint details for ods code: ods_code=YES.` | Confirmation from spine route lookup, ods code set to `yes` to communicate to spine |
| 4 | `Looking up endpoint details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05.` | Request made to routing details from spine route lookup |
| 5 | `Retrieved endpoint details for details="{'service_id': 'urn:nhs:names:services:psis:REPC_IN150016UK05', 'url': 'https://192.168.128.11/reliablemessaging/reliablerequest', 'party_key': 'YES-0000806', 'cpa_id': 'S20001A000182', 'to_asid': '227319907548'}"` | Confirmation endpoint successfully retrieved routing details from spine route lookup |
| 6 | `Looking up reliability details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05.` | Request made to reliability details from spine route lookup |
| 7 | `Retrieved reliability details for service_id=urn:nhs:names:services:psis:REPC_IN150016UK05. reliability_details="{'nhsMHSSyncReplyMode': 'MSHSignalsOnly', 'nhsMHSRetryInterval': 'PT1M', 'nhsMHSRetries': '2', 'nhsMHSPersistDuration': 'PT5M', 'nhsMHSDuplicateElimination': 'always', 'nhsMHSAckRequested': 'always'}"` | Confirmation endpoint successfully reliability details from spine route lookup |
| 8 | `Message serialised successfully` | Serialize outbound message with routing information and previous incoming message data such as `message_id`, `correlation_id`, `interaction_details`, `payload`, `wdo`,`to_party_key`, `cpa_id` |
| 9 | `Attempting to publish work description key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | Attempts to publish the local state of the work description to the state store for new message to outbound with spine route lookup workflow completed|
| 10 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 11 | `No previous version found, continuing attempt to publish new version` | Checks versions to avoid collisions. No remote version found, continues attempt to publish new remote version with current timestamp |
| 12 | `Successfully updated work description to state store for key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | State: VERSION: `1`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_RECEIVED` |
| 13 | `About to make outbound request` | Starting process to send message request from Outbound to Spine |
| 14 | `WorkflowName=async-reliable outbound workflow invoked. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_ACKD received.` | Message successfully sent to spine from outbound and spine returned acknowledgement |
| 15 | `Attempting to publish work description key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | Attempts to publish the local state of the work description to the state store to update message state from this information received spine |
| 16 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 17 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 18 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number
| 19 | `Successfully updated work description to state store for key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | State: VERSION: `2`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_PREPARED` |
| 20 | `Attempting to retrieve the async response from the async store` | Starting process to retrieve message from sync-async store |
| 21 | `Beginning async retrieval from sync-async store` | Retrieval process for sync-async store started |
| 22 | `Entered sync-async inbound workflow` | Started inbound workflow sync-async to handle incoming message |
| 23 | `Attempting to publish work description key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | Attempts to publish the local state of the work description to the state store to update message state received by inbound. |
| 24 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 25 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 26 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 27 | `Successfully updated work description to state store for key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | State: VERSION: `3`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 28 | `Attempting to add inbound message to sync-async store` | Attempt to add incoming message to sync-async store  |
| 29 | `Successfully updated state store` | Sync-async store successfully updated |
| 30 | `Placed message in sync-async store successfully` | Confirmation message successfully added to sync-async store |
| 31 | `Attempting to publish work description key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | Attempts to publish the local state of the work description to the state store to update message state placed in sync-async store. |
| 32 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 33 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 34 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 35 | `Successfully updated work description to state store for key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | State: VERSION: `4`, INBOUND_STATUS: `INBOUND_RESPONSE_RECEIVED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |
| 36 | `Retrieved async response from sync-async store` | Message retrieved by inbound from sync-async store |
| 37 | `Attempting to publish work description key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | Attempts to publish the local state of the work description to the state store to update message state successfully retrieved message from sync-async store |
| 38 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 39 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 40 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, incrementing local version number |
| 41 | `Successfully updated work description to state store for key=2FBB3940-B8DC-481F-8EF0-22CFB5F3D724` | State: VERSION: `5`, INBOUND_STATUS: `INBOUND_RESPONSE_SUCCESSFULLY_PROCESSED`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_ACKD` |

#### Synchronous

| No. | Log Line |  Description | 
| --- | -------- | -----------  | 
| 1 | `Entered sync workflow for outbound message` | Started Outbound sync workflow started to handle incoming message |
| 2 | `Attempting to publish work description key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | Attempts to publish the local state of the work description to the state store for new message to outbound |
| 3 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 4 | `No previous version found, continuing attempt to publish new version` | Checks versions to avoid collisions. No remote version found, continues attempt to publish new remote version with current timestamp |
| 5 | `Successfully updated work description to state store for key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | State: VERSION: `1`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_RECEIVED` |
| 6 | `Looking up endpoint details for ods code: ods_code=YES.` | Confirmation from spine route lookup, ods code set to `yes` to communicate to spine |
| 7 | `Looking up endpoint details for service_id=urn:nhs:names:services:pdsquery:QUPA_IN040000UK32` | Request made to routing details from spine route lookup |
| 8 | `Retrieved endpoint details for details="{'service_id': 'urn:nhs:names:services:pdsquery:QUPA_IN040000UK32', 'url': 'https://192.168.128.11/sync-service', 'party_key': 'YES-0000806', 'cpa_id': 'S20001A000168', 'to_asid': '928942012545'}"` | Confirmation endpoint successfully retrieved routing details from spine route lookup | 
| 9 | `Attempting to publish work description key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | Attempts to publish the local state of the work description to the state store to update message state from this information received spine |
| 10 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 11 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 12 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, increments local version number | 
| 13 | `Successfully updated work description to state store for key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | State: VERSION: `2`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_PREPARED` | 
| 14 | `About to make outbound request` | Starting process to send message request from Outbound to Spine |
| 15 | `Outbound Synchronous workflow completed. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_RESPONSE_RECEIVED received.` | Message successfully sent to spine from outbound and spine returned acknowledgement | 
| 16 | `Attempting to publish work description key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | Attempts to publish the local state of the work description to the state store to update message state from this information received spine |
| 17 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 18 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 19 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, increments local version number | 
| 20 | `Successfully updated work description to state store for key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | State: VERSION: `3`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `OUTBOUND_MESSAGE_RESPONSE_RECEIVED` | 
| 21 | `Outbound Synchronous workflow completed. Message sent to Spine and Acknowledgment=MessageStatus.OUTBOUND_MESSAGE_RESPONSE_RECEIVED received.` | Message successfully received from spine to outbound | 
| 22 | `Attempting to publish work description key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | Attempts to publish the local state of the work description to the state store to update message state from this information received spine |
| 23 | `Retrieving latest work description to check version` | Queries state database with local state to check remote state exists |
| 24 | `Retrieved previous version, comparing versions` | Previous remote version found in state database and comparing versions |
| 25 | `Local version matches remote, incrementing local version number` | Checks versions to avoid collisions. Previous remote version matches local version, increments local version number | 
| 26 | `Successfully updated work description to state store for key=C78164D9-A1EB-497E-BCB5-74CABD3162F0` | State: VERSION: `4`, INBOUND_STATUS: `NULL`, OUTBOUND_STATUS: `SYNC_RESPONSE_SUCCESSFUL` | 

### Cloud Watch

See below example to write CloudWatch queries to parse logs and search for a given correlation id and filter out healthchecks. 

 `parse '* | * | * | * | * | * | * | * | *' as timestamp, level, correlation_id, message_id, interaction_id, inbound_message_id, process, name, text `<br>
 `| display timestamp, level, correlation_id, name, text, message_id`<br>
 `| filter text not like 'healthcheck'`<br>
 `| filter correlation_id = '7'`<br>
 `| filter level = 'INFO'`<br>
 `| limit 10`<br>
 
 Parse query in Cloud Watch add `*` for each value wanted such as timestamp, correlation id etc. Multiple values selected are separated by `|`.
 
 Display selected values columns by using keyword `display` and selecting values such as `timestamp`.
 
 Filter search by given value, use keyword `filter` select a value `correlation_id`, choose an operator `=` and add correlation id value wanted `7`.
 
 Limit number of results return using keyword `limit` and the number of results needed, in this example `10`.
