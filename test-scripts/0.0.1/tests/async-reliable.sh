#!/bin/bash

source ../../export-env-vars.sh

set -ex

UUID1=`uuidgen`
UUID2=`uuidgen`
UUID3=`uuidgen`

curl -i --request POST \
  --url http://localhost:80/ \
  --header 'content-type: application/json' \
  --header 'interaction-id: REPC_IN150016UK05' \
  --header 'sync-async: true' \
  --data '{"payload": "<REPC_IN150016UK05 ITSVersion=\"XML_1.0\"\r\n xmlns=\"urn:hl7-org:v3\">\r\n <id root=\"'$UUID1'\"/>\r\n <creationTime value=\"20190927152035\"/>\r\n <versionCode code=\"V3NPfIT4.2.00\"/>\r\n <interactionId root=\"2.16.840.1.113883.2.1.3.2.4.12\" extension=\"REPC_IN150016UK05\"/>\r\n <processingCode code=\"P\"/>\r\n <processingModeCode code=\"T\"/>\r\n <acceptAckCode code=\"NE\"/>\r\n <communicationFunctionRcv typeCode=\"RCV\">\r\n <device classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"227319907548\"/>\r\n </device>\r\n </communicationFunctionRcv>\r\n <communicationFunctionSnd typeCode=\"SND\">\r\n <device classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"'$FROM_ASID'\"/>\r\n </device>\r\n </communicationFunctionSnd>\r\n <ControlActEvent classCode=\"CACT\" moodCode=\"EVN\">\r\n <author1 typeCode=\"AUT\">\r\n <AgentSystemSDS classCode=\"AGNT\">\r\n <agentSystemSDS classCode=\"DEV\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.107\" extension=\"'$FROM_ASID'\"/>\r\n </agentSystemSDS>\r\n </AgentSystemSDS>\r\n </author1>\r\n <author typeCode=\"AUT\">\r\n <AgentPersonSDS classCode=\"AGNT\">\r\n <id root=\"1.2.826.0.1285.0.2.0.67\" extension=\"055888118514\"/>\r\n <agentPersonSDS classCode=\"PSN\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.65\" extension=\"979603625513\"/>\r\n </agentPersonSDS>\r\n <part typeCode=\"PART\">\r\n <partSDSRole classCode=\"ROL\">\r\n <id extension=\"R0260\" root=\"1.2.826.0.1285.0.2.1.104\"/>\r\n </partSDSRole>\r\n </part>\r\n </AgentPersonSDS>\r\n </author>\r\n <subject typeCode=\"SUBJ\" contextConductionInd=\"false\">\r\n <GPSummary classCode=\"COMPOSITION\" moodCode=\"EVN\">\r\n <id root=\"'$UUID2'\"/>\r\n <code code=\"196981000000101\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.15\" displayName=\"General Practice Summary\"/>\r\n <effectiveTime value=\"20190927152035\"/>\r\n <statusCode code=\"active\"/>\r\n <author typeCode=\"AUT\" contextControlCode=\"OP\">\r\n <time value=\"20190927152035\"/>\r\n <UKCT_MT160018UK01.AgentPersonSDS classCode=\"AGNT\"\r\n xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\r\n <id root=\"1.2.826.0.1285.0.2.0.67\" extension=\"055888118514\"/>\r\n <agentPersonSDS classCode=\"PSN\" determinerCode=\"INSTANCE\">\r\n <id root=\"1.2.826.0.1285.0.2.0.65\" extension=\"979603625513\"/>\r\n <name>\r\n <family>NICA_Test_Automation_Healthchecks</family>\r\n </name>\r\n </agentPersonSDS>\r\n </UKCT_MT160018UK01.AgentPersonSDS>\r\n </author>\r\n <excerptFrom typeCode=\"XCRPT\" inversionInd=\"false\" contextConductionInd=\"true\" negationInd=\"false\">\r\n <templateId root=\"2.16.840.1.113883.2.1.3.2.4.18.2\" extension=\"CSAT_RM-NPfITUK10.excerptFrom\"/>\r\n <seperatableInd value=\"false\"/>\r\n <UKCT_MT144051UK01.CareProfessionalDocumentationCRE classCode=\"CATEGORY\" moodCode=\"EVN\">\r\n <code code=\"163171000000105\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.15\" displayName=\"Care Professional Documentation\"/>\r\n <component typeCode=\"COMP\" inversionInd=\"false\" negationInd=\"false\">\r\n <templateId root=\"2.16.840.1.113883.2.1.3.2.4.18.2\" extension=\"CSAB_RM-NPfITUK10.component\"/>\r\n <seperatableInd value=\"false\"/>\r\n <presentationText classCode=\"OBS\" moodCode=\"EVN\">\r\n <value mediaType=\"text/plain\">\r\n Payload stuff\r\n </value>\r\n <id root=\"'$UUID3'\"/>\r\n <code code=\"PresentationText\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.17.126\" displayName=\"Presentation Text\"/>\r\n <statusCode code=\"completed\"/>\r\n <effectiveTime value=\"20190927152035\"/>\r\n </presentationText>\r\n </component>\r\n </UKCT_MT144051UK01.CareProfessionalDocumentationCRE>\r\n </excerptFrom>\r\n <pertinentInformation1 typeCode=\"PERT\" inversionInd=\"false\" contextConductionInd=\"true\" negationInd=\"false\">\r\n <templateId root=\"2.16.840.1.113883.2.1.3.2.4.18.2\" extension=\"CSAB_RM-NPfITUK10.pertinentInformation1\"/>\r\n <seperatableInd value=\"true\"/>\r\n <pertinentRootCREType classCode=\"CATEGORY\" moodCode=\"EVN\">\r\n <code code=\"163171000000105\" codeSystem=\"2.16.840.1.113883.2.1.3.2.4.15\" displayName=\"Care Professional Documentation\"/>\r\n </pertinentRootCREType>\r\n </pertinentInformation1>\r\n <recordTarget typeCode=\"RCT\">\r\n <patient classCode=\"PAT\">\r\n <id root=\"2.16.840.1.113883.2.1.4.1\" extension=\"9446245796\"/>\r\n </patient>\r\n </recordTarget>\r\n </GPSummary>\r\n </subject>\r\n </ControlActEvent>\r\n </REPC_IN150016UK05>\r\n"}'
