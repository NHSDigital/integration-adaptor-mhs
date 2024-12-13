import os
from pathlib import Path
from unittest import TestCase

from defusedxml import ElementTree

from mhs_common.messages import ebxml_envelope
from utilities import file_utilities

EXPECTED_MESSAGES_DIR = "expected_messages"
MESSAGE_DIR = "test_messages"

MOCK_UUID = "5BB171D4-53B2-4986-90CF-428BE6D157F5"
MOCK_TIMESTAMP = "2012-03-15T06:51:08Z"

BASE_EXPECTED_VALUES = {
    ebxml_envelope.FROM_PARTY_ID: "YES-0000806",
    ebxml_envelope.TO_PARTY_ID: "A91424-9199121",
    ebxml_envelope.CPA_ID: "S1001A1630",
    ebxml_envelope.CONVERSATION_ID: "10F5A436-1913-43F0-9F18-95EA0E43E61A",
    ebxml_envelope.SERVICE: "urn:nhs:names:services:psis",
    ebxml_envelope.ACTION: "MCCI_IN010000UK13",
    ebxml_envelope.MESSAGE_ID: "C614484E-4B10-499A-9ACD-5D645CFACF61",
    ebxml_envelope.TIMESTAMP: "2019-05-04T20:55:16Z",
    ebxml_envelope.RECEIVED_MESSAGE_ID: "F106022D-758B-49A9-A80A-8FF211C32A43"
}


class BaseTestEbxmlEnvelope(TestCase):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    message_dir = Path(current_dir) / MESSAGE_DIR
    expected_message_dir = Path(current_dir) / EXPECTED_MESSAGES_DIR


class TestEbxmlEnvelope(BaseTestEbxmlEnvelope):
    def test_cant_find_optional_text_value_during_parsing(self):
        message = file_utilities.get_file_string(str(self.message_dir / "ebxml_header.xml"))

        xml_tree = ElementTree.fromstring(message)
        values_dict = {}
        ebxml_envelope.EbxmlEnvelope._add_if_present(
            values_dict,
            'key',
            ebxml_envelope.EbxmlEnvelope._extract_ebxml_text_value(xml_tree, 'nonExistentElement')
        )

        self.assertEqual({}, values_dict)

    def test_filename_contains_equals_sign(self):
        expected_external_attachment = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'Filename="735BB673-D9C0-4B85-951E-98DD045C4713_adrian=marbles2.BMP" '
                           'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No '
                           'OriginalBase64=No Length=3345444',
            'title': '"735BB673-D9C0-4B85-951E-98DD045C4713_adrian=marbles2.BMP"'
        }

        description = ('Filename="735BB673-D9C0-4B85-951E-98DD045C4713_adrian=marbles2.BMP" '
                       'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No OriginalBase64=No '
                       'Length=3345444')

        xml_tree = self.generate_soap_envelope_from_description(description)

        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']

        self.assertEqual(external_attachments[0], expected_external_attachment)

    def test_description_does_not_contain_filename(self):
        expected_external_attachment = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No '
                           'OriginalBase64=No Length=3345444',
            'title': None
        }

        description = (
            'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No OriginalBase64=No '
            'Length=3345444'
        )

        xml_tree = self.generate_soap_envelope_from_description(description)
        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']

        self.assertEqual(external_attachments[0], expected_external_attachment)

    def test_description_contains_filename_in_uppercase(self):
        expected_external_attachment = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'FILENAME="735BB673-D9C0-4B85-951E-98DD045C4713_adrian=marbles2.BMP" '
                           'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No '
                           'OriginalBase64=No Length=3345444',
            'title': None
        }

        description = (
            'FILENAME="735BB673-D9C0-4B85-951E-98DD045C4713_adrian=marbles2.BMP" '
            'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No OriginalBase64=No '
            'Length=3345444'
        )

        xml_tree = self.generate_soap_envelope_from_description(description)

        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']

        self.assertEqual(external_attachments[0], expected_external_attachment)

    def test_description_is_not_a_valid_gp2gp_message(self):
        expected_external_attachment = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'This is not a valid GP2GP Message',
            'title': None
        }

        description = 'This is not a valid GP2GP Message'

        xml_tree = self.generate_soap_envelope_from_description(description)

        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']

        self.assertEqual(external_attachments[0], expected_external_attachment)

    def test_description_contains_duplicated_filename_key(self):
        expected_external_attachment = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'Filename="marbles.BMP" Filename="marbles2.BMP" '
                           'ContentType=application/octet-stream Compressed=Yes LargeAttachment=No '
                           'OriginalBase64=No Length=3345444',
            'title': '"marbles2.BMP"'
        }

        description = (
            'Filename="marbles.BMP" Filename="marbles2.BMP" ContentType=application/octet-stream '
            'Compressed=Yes LargeAttachment=No OriginalBase64=No Length=3345444'
        )

        xml_tree = self.generate_soap_envelope_from_description(description)

        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']

        self.assertEqual(external_attachments[0], expected_external_attachment)

    @staticmethod
    def generate_soap_envelope_from_description(description):
        message = '''
            <soap:Envelope xmlns:eb="http://www.oasis-open.org/committees/ebxml-msg/schema/msg-header-2_0.xsd"
                       xmlns:hl7ebxml="urn:hl7-org:transport/ebxml/DSTUv1.0"
                       xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Header>
            <eb:MessageHeader eb:version="2.0" soap:mustUnderstand="1">
            <eb:From>
              <eb:PartyId eb:type="urn:nhs:names:partyType:ocs+serviceInstance">C88046-807354</eb:PartyId>
            </eb:From>
            <eb:To>
              <eb:PartyId eb:type="urn:nhs:names:partyType:ocs+serviceInstance">P83007-822482</eb:PartyId>
            </eb:To>
            <eb:CPAId>d434c95b662b941a59f9</eb:CPAId>
            <eb:ConversationId>A0000131-351C-452F-BEDB-3ED4759A0800</eb:ConversationId>
            <eb:Service>urn:nhs:names:services:gp2gp</eb:Service>
            <eb:Action>RCMR_IN030000UK07</eb:Action>
            <eb:MessageData>
              <eb:MessageId>F01D21CB-31A3-49C6-B0FC-A64C858149AA</eb:MessageId>
              <eb:Timestamp>2024-12-10T08:02:33.405Z</eb:Timestamp>
              <eb:TimeToLive>2024-12-10T14:17:33.405Z</eb:TimeToLive>
            </eb:MessageData>
            <eb:DuplicateElimination />
            </eb:MessageHeader>
            <eb:AckRequested eb:version="2.0" soap:mustUnderstand="1"
                 soap:actor="urn:oasis:names:tc:ebxml-msg:actor:nextMSH" eb:signed="false" />
            </soap:Header>
            <soap:Body>
              <eb:Manifest eb:version="2.0" soap:mustUnderstand="1">
                <eb:Reference xlink:href="cid:Content1@e-mis.com/EMISWeb/GP2GP2.2A"
                      xmlns:xlink="http://www.w3.org/1999/xlink">
                  <eb:Description xml:lang="en">RCMR_IN030000UK07</eb:Description>
                  <hl7ebxml:Payload style="HL7" encoding="XML" version="3.0" />
                </eb:Reference>
                <eb:Reference xlink:href="mid:E54DEC57-6BA5-40AB-ACD0-1E383209C034"
                      eb:id="_735BB673-D9C0-4B85-951E-98DD045C4713"
                      xmlns:xlink="http://www.w3.org/1999/xlink">
                <eb:Description xml:lang="en">%s</eb:Description>
                </eb:Reference>
              </eb:Manifest>
            </soap:Body>
            </soap:Envelope>''' % description

        xml_tree = ElementTree.fromstring(message)
        return xml_tree
