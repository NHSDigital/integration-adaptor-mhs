#!/bin/bash

#source ../../export-env-vars.sh

set -ex

#UUID=`uuidgen`
#
#curl -i --request POST \
#  --url http://localhost:80/ \
#  --header 'content-type: application/json' \
#  --header 'interaction-id: COPC_IN000001UK01' \
#  --header 'ods-code: X26' \
#  --header 'wait-for-response: false' \
#  --data '{"payload": "<COPC_IN000001UK01 xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns=\"urn:hl7-org:v3\">\r\n <id root=\"'$UUID'\" />\r\n <creationTime value=\"20190927152035\" />\r\n <versionCode code=\"3NPfIT7.2.02\" />\r\n <interactionId root=\"2.16.840.1.113883.2.1.3.2.4.12\" extension=\"COPC_IN000001UK01\" />\r\n <processingCode code=\"P\" />\r\n <processingModeCode code=\"T\" />\r\n <acceptAckCode code=\"NE\" />\r\n <communicationFunctionRcv type=\"CommunicationFunction\" typeCode=\"RCV\">\r\n <device type=\"Device\" classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"918999198982\" />\r\n </device>\r\n </communicationFunctionRcv>\r\n <communicationFunctionSnd type=\"CommunicationFunction\" typeCode=\"SND\">\r\n <device type=\"Device\" classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"918999198982\" />\r\n </device>\r\n </communicationFunctionSnd>\r\n <ControlActEvent classCode=\"OBS\" moodCode=\"EVN\">\r\n <author1 type=\"Participation\" typeCode=\"AUT\">\r\n <AgentSystemSDS type=\"RoleHeir\" classCode=\"AGNT\">\r\n <agentSystemSDS type=\"Device\" classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"918999198982\" />\r\n </agentSystemSDS>\r\n </AgentSystemSDS>\r\n </author1>\r\n <subject typeCode=\"SUBJ\" contextConductionInd=\"false\">\r\n <PayloadInformation classCode=\"OBS\" moodCode=\"EVN\">\r\n <code code=\"GP2GPLMATTACHMENTINFO\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.17.202\" displayName=\"GP2GP Large Message Attachment Information\" />\r\n <id root=\"528e7a06-e407-442b-9635-28626fe2205a\" />\r\n <messageType root=\"2.16.840.1.113883.2.1.3.2.4.18.17\" extension=\"RCMR_MT000001GB01\" xmlns=\"NPFIT:HL7:Localisation\" />\r\n <value>\r\n <Gp2gpfragment xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"urn:nhs:names:services:gp2gp\">\r\n <Version xsi:type=\"xsd:string\">01</Version>\r\n <Recipients>\r\n <Recipient>X26-9199246</Recipient>\r\n </Recipients>\r\n <From>918999198982</From>\r\n <subject>Attachment:test file will go here</subject>\r\n <message-id>02dc2581-82b0-47af-b9a6-46e8d536ab2e</message-id>\r\n </Gp2gpfragment>\r\n </value>\r\n <pertinentInformation typeCode=\"PERT\">\r\n <sequenceNumber value=\"1\" />\r\n <pertinentPayloadBody classCode=\"OBS\" moodCode=\"EVN\">\r\n <code code=\"GP2GPLMATTACHMENT\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.17.202\" displayName=\"GP2GP Large Message Attachment\" />\r\n <id root=\"a24ef71e-72df-4f3d-80d1-d23ff846600f\" />\r\n <value>\r\n <reference value=\"file://localhost/1E49E84D-B29B-466B-93A5-432459CA549B_Treadmill%20Running%20300fps_12.avi\" />\r\n </value>\r\n </pertinentPayloadBody>\r\n </pertinentInformation>\r\n </PayloadInformation>\r\n </subject>\r\n </ControlActEvent>\r\n </COPC_IN000001UK01>"}'

source common.sh

UUID=$(uuidgen)
export UUID
INTERACTION_ID=COPC_IN000001UK01
WAIT_FOR_RESPONSE="${1:-false}"

REQUEST_BODY="$(request_body_from_xml_file forward-reliable.xml)"

mhs_request