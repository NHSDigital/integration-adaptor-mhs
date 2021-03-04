# Test Scripts

You can use these `bash` shell scripts to smoke test the MHS adaptor.

## Prerequisites

The following commands must exist to run the scripts:

* `curl` sends the outbound http requests
* `python` constructs the payload for the JSON request.
* `uuidgen` generates unique random identifiers for outbound messages.
* `envsubst` substitutes values in the xml message templates

## async-express.sh

`./async-express.sh` sends the message `async-express.xml`. The first (optional) 
argument enables sync-async (wait-for-response) e.g. `./async-express.sh true`

## async-reliable.sh

`./async-reliable.sh` sends the message `async-reliable.xml`. The first (optional) 
argument enables sync-async (wait-for-response) e.g. `./async-reliable.sh true`

## sync.sh

`./sync.sh` ends the message `sync.xml`.

## forward-reliable.sh

`./forward-reliable.sh` sends the message `forward-reliable.xml`. Set the 
`export-env-vars.sh` variable `FROM_ODS_CODE` to your ODS code to also receive an 
inbound forward reliable message. This configuration sends the forward reliable 
message to yourself.

## rabbit_to_xml.sh

The `rabbit_to_xml.sh` helper script decodes asynchronous replies published to 
the inbound queue when using RabbitMQ. From the RabbitMQ web console copy the
base64 text content to a file. The script extracts the XML of the payload.

Usage: `rabbit_to_xml.sh reply.txt > reply.xml`