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

CREATION_TIME=$(date +%Y%m%d%H%M%S)
export CREATION_TIME

random_uuid() {
  UUID=$(uuidgen)
  echo "$UUID" | tr a-z A-Z
}

json_escape () {
    printf '%s' "$1" | python -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

request_body_from_file() {
  envsubst < "$1"
}

request_body_from_xml_file() {
  EHR_EXTRACT="$(request_body_from_file "$1")"
  PAYLOAD=$(json_escape "$EHR_EXTRACT")
  echo "{\"payload\":$PAYLOAD}"
}

WAIT_FOR_RESPONSE="false"

mhs_request() {
  curl -i -k -v -X POST \
    -H "Content-Type: application/json" \
    -H "Interaction-Id: $INTERACTION_ID" \
    -H "from-asid: $FROM_ASID" \
    -H "wait-for-response: $WAIT_FOR_RESPONSE" \
    -H "Correlation-Id: $(uuidgen)" \
    -d "$REQUEST_BODY" \
    "$MHS_OUTBOUND_URL"
}

mhs_request_ods() {
  curl -i -k -v -X POST \
    -H "Content-Type: application/json" \
    -H "Interaction-Id: $INTERACTION_ID" \
    -H "from-asid: $FROM_ASID" \
    -H "wait-for-response: $WAIT_FOR_RESPONSE" \
    -H "Correlation-Id: $(uuidgen)" \
    -H "ods-code: $FROM_ODS_CODE" \
    -d "$REQUEST_BODY" \
    "$MHS_OUTBOUND_URL"
}

mhs_request_inbound() {
  echo "${MHS_SECRET_CLIENT_CERT}" > client.crt
  echo "${MHS_SECRET_CLIENT_KEY}" > client.key
  echo "${MHS_SECRET_CA_CERTS}" > ca.crt
  curl -i -k -v -X POST \
    --cert client.crt --key client.key --cacert ca.crt \
    -H "Content-Type: multipart/related; boundary=\"--=_MIME-Boundary\"; type=\"text/xml\"; start=\"<ebXMLHeader@spine.nhs.uk>\"" \
    -H "SOAPAction: urn:nhs:names:services:gp2gp/COPC_IN000001UK01" \
    -d "$REQUEST_BODY" \
    "$MHS_INBOUND_URL"
}