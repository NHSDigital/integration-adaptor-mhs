#!/usr/bin/env bash
# Common helpers for the test scripts. Don't execute this script directly.

RED='\033[31m'
NC='\033[0m'

if [ -f "../export-env-vars.sh" ]; then
    source ../export-env-vars.sh
else
  echo "${RED}ERROR: Missing export-env-vars.sh file${NC}"
  exit 1
fi

CREATION_TIME=$(date +%Y%d%m%H%M%S000)
export CREATION_TIME

json_escape () {
    printf '%s' "$1" | python -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

request_body_from_xml_file() {
  EHR_EXTRACT="$(envsubst < "$1")"
  PAYLOAD=$(json_escape "$EHR_EXTRACT")
  echo "{\"payload\":$PAYLOAD}"
}

mhs_request() {
  curl -i -k -v -X POST \
    -H "Content-Type: application/json" \
    -H "Interaction-Id: $INTERACTION_ID" \
    -H "from-asid: $FROM_ASID" \
    -H "wait-for-response: false" \
    -H "Correlation-Id: $(uuidgen)" \
    ${EXTRA_CURL_OPTS} \
    -d "$REQUEST_BODY" \
    "$MHS_OUTBOUND_URL"
}