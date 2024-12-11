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
        expected_external_attachment1 = {
            'document_id': 'EB653254-7854-450E-A3D3-B1711D99D665_adrian=marbles.BMP',
            'message_id': 'MESSAGE GOES HERE',
            'description': 'DESCRIPTION GOES HERE',
            'title': 'EB653254-7854-450E-A3D3-B1711D99D665_adrian=marbles.BMP'
        },
        expected_external_attachment2 = {
            'document_id': '_735BB673-D9C0-4B85-951E-98DD045C4713',
            'message_id': 'E54DEC57-6BA5-40AB-ACD0-1E383209C034',
            'description': 'DESCRIPTION GOES HERE',
            'title': 'EB653254-7854-450E-A3D3-B1711D99D665_adrian=marbles.BMP'
        }

        message = file_utilities.get_file_string(
            str(self.message_dir / "ebxml_request_manifest_contains_filename_with_equals.xml")
        )
        xml_tree = ElementTree.fromstring(message)

        external_attachments = ebxml_envelope.EbxmlEnvelope.parse_external_attachments(xml_tree)['external_attachments']
        self.assertEqual(external_attachments[0], expected_external_attachment1)

