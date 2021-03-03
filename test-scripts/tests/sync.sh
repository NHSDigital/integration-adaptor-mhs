#!/bin/bash

source common.sh

set -ex

UUID=$(random_uuid)
export UUID
REQUEST_BODY="$(request_body_from_xml_file sync.xml)"
INTERACTION_ID=QUPA_IN040000UK32

mhs_request
