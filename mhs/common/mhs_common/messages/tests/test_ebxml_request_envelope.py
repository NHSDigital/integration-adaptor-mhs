import copy
from unittest.mock import patch

from builder import pystache_message_builder
from utilities import file_utilities
from utilities import message_utilities

import mhs_common.messages.ebxml_envelope as ebxml_envelope
import mhs_common.messages.ebxml_request_envelope as ebxml_request_envelope
import mhs_common.messages.tests.test_ebxml_envelope as test_ebxml_envelope

EXPECTED_EBXML = "ebxml_request.xml"

CONTENT_TYPE_HEADER_NAME = "Content-Type"
MULTIPART_MIME_HEADERS = {CONTENT_TYPE_HEADER_NAME: 'multipart/related; boundary="--=_MIME-Boundary"'}
EXPECTED_MESSAGE = '<hl7:MCCI_IN010000UK13 xmlns:hl7="urn:hl7-org:v3"/>'

_ADDITIONAL_EXPECTED_VALUES = {
    ebxml_request_envelope.DUPLICATE_ELIMINATION: True,
    ebxml_request_envelope.SYNC_REPLY: True,
    ebxml_request_envelope.ACK_REQUESTED: True,
    ebxml_request_envelope.ACK_SOAP_ACTOR: "urn:oasis:names:tc:ebxml-msg:actor:toPartyMSH",
    ebxml_request_envelope.ATTACHMENTS: [],
    ebxml_request_envelope.EXTERNAL_ATTACHMENTS: []
}
EXPECTED_VALUES = {**test_ebxml_envelope.BASE_EXPECTED_VALUES, **_ADDITIONAL_EXPECTED_VALUES}

EXPECTED_HTTP_HEADERS = {
    'charset': 'UTF-8',
    'SOAPAction': 'urn:nhs:names:services:pdsquery/QUPA_IN000006UK02',
    'Content-Type': 'multipart/related; boundary="--=_MIME-Boundary"; type=text/xml; start=ebXMLHeader@spine.nhs.uk'
}

def get_test_message_dictionary():
    return {
        ebxml_envelope.FROM_PARTY_ID: "TESTGEN-201324",
        ebxml_envelope.TO_PARTY_ID: "YEA-0000806",
        ebxml_envelope.CPA_ID: "S1001A1630",
        ebxml_envelope.CONVERSATION_ID: "79F49A34-9798-404C-AEC4-FD38DD81C138",
        ebxml_envelope.SERVICE: "urn:nhs:names:services:pdsquery",
        ebxml_envelope.ACTION: "QUPA_IN000006UK02",
        ebxml_envelope.ATTACHMENTS: [],
        ebxml_envelope.EXTERNAL_ATTACHMENTS: [],
        ebxml_request_envelope.DUPLICATE_ELIMINATION: True,
        ebxml_request_envelope.ACK_REQUESTED: True,
        ebxml_request_envelope.ACK_SOAP_ACTOR: "urn:oasis:names:tc:ebxml-msg:actor:toPartyMSH",
        ebxml_request_envelope.SYNC_REPLY: True,
        ebxml_request_envelope.MESSAGE: '<QUPA_IN000006UK02 xmlns="urn:hl7-org:v3"></QUPA_IN000006UK02>'
    }


def expected_values(ebxml=None, payload=None, attachments=None, external_attachments=None):
    values = copy.deepcopy(EXPECTED_VALUES)

    if ebxml:
        values[ebxml_request_envelope.EBXML] = ebxml
    if payload:
        values[ebxml_request_envelope.MESSAGE] = payload
    if attachments:
        values[ebxml_request_envelope.ATTACHMENTS] += attachments
    if external_attachments:
        values[ebxml_request_envelope.EXTERNAL_ATTACHMENTS] += external_attachments

    return values


class TestEbxmlRequestEnvelope(test_ebxml_envelope.BaseTestEbxmlEnvelope):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalized_expected_serialized_message = self._get_expected_file_string(EXPECTED_EBXML)

    #####################
    # Serialisation tests
    #####################

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_with_no_attachments(self, mock_get_uuid, mock_get_timestamp):
        mock_get_uuid.return_value = test_ebxml_envelope.MOCK_UUID
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        envelope = ebxml_request_envelope.EbxmlRequestEnvelope(get_test_message_dictionary())

        message_id, http_headers, message = envelope.serialize()

        normalized_message = file_utilities.normalize_line_endings(message)

        self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
        self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
        self.assertEqual(self.normalized_expected_serialized_message, normalized_message)

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_with_one_attachment(self, mock_get_uuid, mock_get_timestamp):
        mock_get_uuid.side_effect = ["8F1D7DE1-02AB-48D7-A797-A947B09F347F", test_ebxml_envelope.MOCK_UUID]
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        message_dictionary = get_test_message_dictionary()
        message_dictionary[ebxml_request_envelope.ATTACHMENTS] = [{
            ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
            ebxml_request_envelope.ATTACHMENT_BASE64: False,
            ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description',
            ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
            ebxml_request_envelope.ATTACHMENT_DOCUMENT_ID: []
        }]
        message_dictionary[ebxml_request_envelope.EXTERNAL_ATTACHMENTS] = []
        envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

        message_id, http_headers, message = envelope.serialize()

        normalized_expected_message = self._get_expected_file_string('ebxml_request_one_attachment.xml')
        normalized_message = file_utilities.normalize_line_endings(message)

        self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
        self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
        self.assertEqual(normalized_expected_message, normalized_message)

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_with_one_attachment_with_document_id(self, mock_get_uuid, mock_get_timestamp):
        mock_get_uuid.side_effect = ["8F1D7DE1-02AB-48D7-A797-A947B09F347F", test_ebxml_envelope.MOCK_UUID]
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        message_dictionary = get_test_message_dictionary()
        message_dictionary[ebxml_request_envelope.ATTACHMENTS] = [{
            ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
            ebxml_request_envelope.ATTACHMENT_BASE64: False,
            ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description',
            ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
            ebxml_request_envelope.ATTACHMENT_DOCUMENT_ID: '_some-document-id'
        }]
        message_dictionary[ebxml_request_envelope.EXTERNAL_ATTACHMENTS] = []
        envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

        message_id, http_headers, message = envelope.serialize()

        normalized_expected_message = self._get_expected_file_string(
            'ebxml_request_one_attachment_with_document_id.xml')
        normalized_message = file_utilities.normalize_line_endings(message)

        self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
        self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
        self.assertEqual(normalized_expected_message, normalized_message)

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_with_multiple_attachments(self, mock_get_uuid, mock_get_timestamp):
        mock_get_uuid.side_effect = [
            "8F1D7DE1-02AB-48D7-A797-A947B09F347F", "64A73E03-30BD-4231-9959-0C4B54400345",
            test_ebxml_envelope.MOCK_UUID
        ]
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        message_dictionary = get_test_message_dictionary()
        message_dictionary[ebxml_request_envelope.ATTACHMENTS] = [
            {
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description',
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
                ebxml_request_envelope.ATTACHMENT_DOCUMENT_ID: []
            },
            {
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'image/png',
                ebxml_request_envelope.ATTACHMENT_BASE64: True,
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Another description',
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'QW5vdGhlciBwYXlsb2Fk',
                ebxml_request_envelope.ATTACHMENT_DOCUMENT_ID: []
            }
        ]
        envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

        message_id, http_headers, message = envelope.serialize()

        normalized_expected_message = self._get_expected_file_string('ebxml_request_multiple_attachments.xml')
        normalized_message = file_utilities.normalize_line_endings(message)

        self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
        self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
        self.assertEqual(normalized_expected_message, normalized_message)

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_message_id_not_generated(self, mock_get_uuid, mock_get_timestamp):
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        message_dictionary = get_test_message_dictionary()
        message_dictionary[ebxml_envelope.MESSAGE_ID] = test_ebxml_envelope.MOCK_UUID
        envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

        message_id, http_headers, message = envelope.serialize()

        normalized_message = file_utilities.normalize_line_endings(message)

        mock_get_uuid.assert_not_called()
        self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
        self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
        self.assertEqual(self.normalized_expected_serialized_message, normalized_message)

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_raises_error_when_required_tags_not_passed(self, mock_get_uuid, mock_get_timestamp):
        mock_get_uuid.return_value = test_ebxml_envelope.MOCK_UUID
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        keys = set(get_test_message_dictionary().keys())
        keys.remove(ebxml_envelope.ATTACHMENTS)
        keys.remove(ebxml_envelope.EXTERNAL_ATTACHMENTS)

        for required_tag in keys:
            with self.subTest(required_tag=required_tag):
                test_message_dict = get_test_message_dictionary()
                del test_message_dict[required_tag]
                envelope = ebxml_request_envelope.EbxmlRequestEnvelope(test_message_dict)

                with self.assertRaisesRegex(pystache_message_builder.MessageGenerationError, 'Failed to find key'):
                    envelope.serialize()

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_raises_error_when_required_attachment_tags_not_passed(self, mock_get_uuid, mock_get_timestamp):
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        required_tags = [
            ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE, ebxml_request_envelope.ATTACHMENT_BASE64,
            ebxml_request_envelope.ATTACHMENT_DESCRIPTION, ebxml_request_envelope.ATTACHMENT_PAYLOAD
        ]
        for required_tag in required_tags:
            with self.subTest(required_tag=required_tag):
                mock_get_uuid.side_effect = ["8F1D7DE1-02AB-48D7-A797-A947B09F347F", test_ebxml_envelope.MOCK_UUID]

                message_dictionary = get_test_message_dictionary()
                message_dictionary[ebxml_request_envelope.ATTACHMENTS] = [{
                    ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                    ebxml_request_envelope.ATTACHMENT_BASE64: False,
                    ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description',
                    ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload'
                }]
                del message_dictionary[ebxml_request_envelope.ATTACHMENTS][0][required_tag]
                envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

                with self.assertRaisesRegex(pystache_message_builder.MessageGenerationError, 'Failed to find key'):
                    envelope.serialize()

    @patch.object(message_utilities, "get_timestamp")
    @patch.object(message_utilities, "get_uuid")
    def test_serialize_doesnt_include_xml_tag_when_corresponding_boolean_flag_set_to_false(self, mock_get_uuid,
                                                                                           mock_get_timestamp):
        mock_get_uuid.return_value = test_ebxml_envelope.MOCK_UUID
        mock_get_timestamp.return_value = test_ebxml_envelope.MOCK_TIMESTAMP

        test_cases = [
            (ebxml_request_envelope.DUPLICATE_ELIMINATION, 'eb:DuplicateElimination'),
            (ebxml_request_envelope.ACK_REQUESTED, 'eb:AckRequested'),
            (ebxml_request_envelope.SYNC_REPLY, 'eb:SyncReply')
        ]
        for boolean_tag, boolean_xml_tag in test_cases:
            with self.subTest(boolean_tag=boolean_tag):
                message_dictionary = get_test_message_dictionary()
                message_dictionary[boolean_tag] = False
                envelope = ebxml_request_envelope.EbxmlRequestEnvelope(message_dictionary)

                message_id, http_headers, message = envelope.serialize()

                normalized_message = file_utilities.normalize_line_endings(message)

                self.assertEqual(test_ebxml_envelope.MOCK_UUID, message_id)
                self.assertEqual(EXPECTED_HTTP_HEADERS, http_headers)
                self.assertNotEqual(self.normalized_expected_serialized_message, normalized_message)
                self.assertNotIn(boolean_xml_tag, normalized_message)

    #######################
    # Deserialisation tests
    #######################

    def test_from_string_parses_valid_requests(self):
        with self.subTest("A valid request containing a payload"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request')
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A multi-part MIME message with a defect in the payload"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_payload_defect')
            expected_values_with_test_payload = expected_values(ebxml=ebxml, payload="mock-payload")

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_test_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request that does not contain the optional payload MIME part"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_no_payload')
            expected_values_with_no_payload = expected_values(ebxml=ebxml, payload=None)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_no_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one 8-bit encoded textual attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_8bit_attachment')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one 7-bit encoded textual attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_7bit_attachment')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some seven bit payload, limited to US-ASCII characters.',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one binary encoded textual attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_binary_attachment')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload which has a binary encoding.',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request without the Content-Transfer-Encoding header specified"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_no_encoding')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'This inbound message has no Content-Transfer-Encoding headers.',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one textual attachment with application/xml content type"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_attachment_application_xml_content_type')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing multibyte UTF8 characters within HL7 XML"):
            # Regression test for NIAD-2822
            message, _ = message_utilities.load_test_data(self.message_dir, 'ebxml_request_multibyte_character')
            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)
            self.assertEquals(parsed_message.message_dictionary['hl7_message'], "<xml>¬ ❤️ 🧸</xml>")

        with self.subTest(
            "A valid request containing a fragment of a GZIP compressed text/plain file. "
            "Where a fragment is a chunk of a larger file, but needs to be broken up to fit within the 5MB spine limit. "
            "Fragments and compression are a part of the GP2GP Large Messaging specification."):
            message, _ = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_attachment_text_plain_content_compressed_fragment')

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            payload = ( 'jj2Ln886YL4rjojQ7NLcmwWWu9CQMLmgevxThRBIMv501+zRfFB9vFM39baF+uzabvV718ZWbd2nO916'
                        '7phnuAzC57RJyzsN+9ootsm+Q3YLYb9z54riB7z0QbbdbF4br8xN7ZZN3yt2+l2GeY5Z5NL0E0urYFft'
                        '0Gs1rg2ZbRHWlkP+8k4F1s/AD0pTu/kCn7VSG0e64rNbTluj132qP+cLJONT8Z5G5MB4bxr8sVA7elMz'
                        'wOpWYlT9z7FfOu3maYNCqDzA9Ipeza1O5whzpVIRuI16ebPTd66VbpuqTwRIGrw25k81JdbB8t2Hib/S'
                        'cx0vVv8WWPW/Bf8CszTdwWLwb+O/2u1DyfkYAAA=' )

            self.assertEqual([{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: payload,
                ebxml_request_envelope.ATTACHMENT_BASE64: True,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Some description'
            }], parsed_message.message_dictionary['attachments'])

        with self.subTest("A valid request containing one textual attachment with no description provided"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_attachment_application_xml_content_type_no_description')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'Some payload',
                ebxml_request_envelope.ATTACHMENT_BASE64: False,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: ''
            }]

            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one compressed textual attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_attachment_text_plain_content_compressed')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'H4sIAAAAAAAA/3WSzW7sIAyF9zyFd7PJS0xX7aaq1JG6ZsAJdAiOwBlu3v4eyGwrRVGCfzjfsW+BC9O6V6U7U5WV6RGzJ5mp2YNkV7XUc8y3jZ40MP3KgwupjB8NkWdz6xmXikNBLxfISZ73GiWbD3I2X5QWVspChVMvMG+IZq6VVs5T73SQLzE/aD2oIWK+kjTEyMeln7EtGsynZEY4JUr85ESSh4jUCz7lLh6K5xlaPIVYqUnx5p2PCQSHQQaut7UXydDD/1xU9l3+CdITB386qG7gPMnIdo9sPuj8WyUvtFfzE4Rmhg4NVqFiZsKt913JDpdAqRPtYRpnh+xkYe3HRI0vT4bh3PUX2ZcwWphr7hajB54sCvsLzVZhvoBYcSdVlY3UJqi8IJYqQ2uWNiACCjAGsGmExITSF/t7f11hnE1dfHetWXVBpXExX7DecaUHbzpiz8gNeDGBNqUzXfo4nMWGdIrGWc0bjJkFQiuXp81ap74C5odTOrmxPzV62HIOyknymGhVi+vMtY/SO1jnsVpLkZbMrWFIqCiY3vB624pYF4DzcqcvAD7uvNgxyICyF+SffH9G/gMaqXG6/wIAAA==',
                ebxml_request_envelope.ATTACHMENT_BASE64: True,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'text/plain',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Filename="277F29F1-FEAB-4D38-8266-FEB7A1E6227D_LICENSE.txt" ContentType=text/plain Compressed=Yes LargeAttachment=No OriginalBase64=Yes'
            }]

            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one compressed application/xml attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_attachment_application_xml_content_compressed')
            attachments = [{
                ebxml_request_envelope.ATTACHMENT_PAYLOAD: 'H4sIAAAAAAAA/3WSzW7sIAyF9zyFd7PJS0xX7aaq1JG6ZsAJdAiOwBlu3v4eyGwrRVGCfzjfsW+BC9O6V6U7U5WV6RGzJ5mp2YNkV7XUc8y3jZ40MP3KgwupjB8NkWdz6xmXikNBLxfISZ73GiWbD3I2X5QWVspChVMvMG+IZq6VVs5T73SQLzE/aD2oIWK+kjTEyMeln7EtGsynZEY4JUr85ESSh4jUCz7lLh6K5xlaPIVYqUnx5p2PCQSHQQaut7UXydDD/1xU9l3+CdITB386qG7gPMnIdo9sPuj8WyUvtFfzE4Rmhg4NVqFiZsKt913JDpdAqRPtYRpnh+xkYe3HRI0vT4bh3PUX2ZcwWphr7hajB54sCvsLzVZhvoBYcSdVlY3UJqi8IJYqQ2uWNiACCjAGsGmExITSF/t7f11hnE1dfHetWXVBpXExX7DecaUHbzpiz8gNeDGBNqUzXfo4nMWGdIrGWc0bjJkFQiuXp81ap74C5odTOrmxPzV62HIOyknymGhVi+vMtY/SO1jnsVpLkZbMrWFIqCiY3vB624pYF4DzcqcvAD7uvNgxyICyF+SffH9G/gMaqXG6/wIAAA==',
                ebxml_request_envelope.ATTACHMENT_BASE64: True,
                ebxml_request_envelope.ATTACHMENT_CONTENT_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_request_envelope.ATTACHMENT_CONTENT_TYPE: 'application/xml',
                ebxml_request_envelope.ATTACHMENT_DESCRIPTION: 'Filename="277F29F1-FEAB-4D38-8266-FEB7A1E6227D_LICENSE.txt" ContentType=text/plain Compressed=Yes LargeAttachment=No OriginalBase64=Yes'
            }]

            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           attachments=attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)
            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest("A valid request containing one external attachment"):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_one_external_attachment')
            external_attachments = [{
                ebxml_envelope.EXTERNAL_ATTACHMENT_DOCUMENT_ID: '8681AF4F-E577-4C8D-A2CE-43CABE3D5FB4',
                ebxml_envelope.EXTERNAL_ATTACHMENT_MESSAGE_ID: '8F1D7DE1-02AB-48D7-A797-A947B09F347F@spine.nhs.uk',
                ebxml_envelope.EXTERNAL_ATTACHMENT_DESCRIPTION: 'Filename="8F1D7DE1-02AB-48D7-A797-A947B09F347F.txt" ContentType=text/plain Compressed=No LargeAttachment=No OriginalBase64=Yes',
                ebxml_envelope.EXTERNAL_ATTACHMENT_TITLE: '"8F1D7DE1-02AB-48D7-A797-A947B09F347F.txt"'
            }]
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE,
                                                           external_attachments = external_attachments)

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)



    def test_from_string_errors_on_invalid_request(self):
        with self.subTest("A message that is not a multi-part MIME message"):
            with self.assertRaises(ebxml_envelope.EbXmlParsingError):
                ebxml_request_envelope.EbxmlRequestEnvelope.from_string({CONTENT_TYPE_HEADER_NAME: "text/plain"},
                                                                        "A message")

        sub_tests = [
            ("An invalid multi-part MIME message", "ebxml_request_no_header.msg"),
            ("A message with an invalid binary ebXML header", "ebxml_request_invalid_binary_ebxml_header.msg"),
            ("A message with an invalid binary HL7 payload", "ebxml_request_invalid_binary_hl7_payload.msg"),
            ("A message with an invalid application/xml binary HL7 payload",
             "ebxml_request_invalid_application_xml_binary_hl7_payload.msg")
        ]
        for sub_test_name, filename in sub_tests:
            with self.subTest(sub_test_name):
                message = file_utilities.get_file_string(
                    str(self.message_dir / filename))

                with self.assertRaises(ebxml_envelope.EbXmlParsingError):
                    ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

    def test_from_string_parses_messages_with_optional_parts_missing(self):
        sub_tests = [
            ('DuplicateElimination', 'ebxml_request_no_duplicate_elimination', ebxml_request_envelope.DUPLICATE_ELIMINATION),
            ('SyncReply', 'ebxml_request_no_sync_reply', ebxml_request_envelope.SYNC_REPLY)
        ]
        for element_name, filename, key in sub_tests:
            with self.subTest(f'A valid request without a {element_name} element'):
                message, ebxml = message_utilities.load_test_data(self.message_dir, filename)

                expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE)
                expected_values_with_payload[key] = False

                parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(
                    MULTIPART_MIME_HEADERS, message)

                self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest(f'A valid request without an AckRequested element'):
            message, ebxml = message_utilities.load_test_data(self.message_dir, 'ebxml_request_no_ack_requested')
            expected_values_with_payload = expected_values(ebxml=ebxml, payload=EXPECTED_MESSAGE)
            expected_values_with_payload[ebxml_request_envelope.ACK_REQUESTED] = False
            del expected_values_with_payload[ebxml_request_envelope.ACK_SOAP_ACTOR]

            parsed_message = ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

            self.assertEqual(expected_values_with_payload, parsed_message.message_dictionary)

        with self.subTest(f'A valid request without an AckRequested SOAP actor attribute'):
            message, _ = message_utilities.load_test_data(self.message_dir, 'ebxml_request_no_soap_actor')

            with self.assertRaisesRegex(
                    ebxml_envelope.EbXmlParsingError, "Weren't able to find required attribute actor"):
                ebxml_request_envelope.EbxmlRequestEnvelope.from_string(MULTIPART_MIME_HEADERS, message)

    #######################
    # Helper methods
    #######################

    def _get_expected_file_string(self, filename: str):
        # Pystache does not convert line endings to LF in the same way as Python does when loading the example from
        # file, so normalize the line endings of the strings being compared
        return file_utilities.normalize_line_endings(
            file_utilities.get_file_string(str(self.expected_message_dir / filename)))
