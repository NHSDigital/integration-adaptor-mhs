#!/bin/bash

set -ex

source common.sh

UUID1=$(random_uuid)
export UUID1
UUID2=$(random_uuid)
export UUID2
UUID3=$(random_uuid)
export UUID3
INTERACTION_ID=REPC_IN150016UK05
WAIT_FOR_RESPONSE="${1:-false}"

REQUEST_BODY="$(request_body_from_xml_file async-reliable.xml)"

mhs_request