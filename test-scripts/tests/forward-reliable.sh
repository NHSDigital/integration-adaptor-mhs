#!/bin/bash

set -ex

source common.sh

UUID=$(random_uuid)
export UUID
INTERACTION_ID=COPC_IN000001UK01
WAIT_FOR_RESPONSE="${1:-false}"

REQUEST_BODY="$(request_body_from_xml_file forward-reliable.xml)"

mhs_request_ods