#!/bin/bash

source common.sh

set -ex

UUID=$(uuidgen)
REQUEST_BODY="$(request_body_from_xml_file sync.xml)"
INTERACTION_ID=QUPA_IN040000UK32

mhs_request
