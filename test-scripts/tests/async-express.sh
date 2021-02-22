#!/bin/bash

set -ex

source common.sh

UUID=$(random_uuid)
export UUID
INTERACTION_ID=QUPC_IN160101UK05
WAIT_FOR_RESPONSE="${1:-false}"

REQUEST_BODY="$(request_body_from_xml_file async-express.xml)"

mhs_request