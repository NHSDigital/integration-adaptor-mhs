#!/bin/bash

set -ex

source common.sh

CONVERSATION_ID=$(random_uuid)
export CONVERSATION_ID
MESSAGE_ID=$(random_uuid)
export MESSAGE_ID

REQUEST_BODY="$(request_body_from_file inbound-unsolicited.txt)"

mhs_request_inbound
