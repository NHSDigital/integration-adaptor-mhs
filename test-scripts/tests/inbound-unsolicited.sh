#!/bin/bash

set -ex

source common.sh

UUID=$(random_uuid)
export UUID

REQUEST_BODY="$(request_body_from_file inbound-unsolicited.txt)"

mhs_request_inbound
