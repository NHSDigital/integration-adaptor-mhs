"""Component tests related to the forward-reliable message pattern"""

import unittest

from integration_tests.amq.amq_message_assertor import AMQMessageAssertor
from integration_tests.amq.mhs_inbound_queue import MHS_INBOUND_QUEUE
from integration_tests.assertors.json_error_response_assertor import JsonErrorResponseAssertor
from integration_tests.db.db_wrapper_factory import MHS_STATE_TABLE_WRAPPER, MHS_SYNC_ASYNC_TABLE_WRAPPER
from integration_tests.db.mhs_table import MhsTableStateAssertor
from integration_tests.helpers.build_message import build_message
from integration_tests.http.inbound_proxy_http_request_builder import InboundProxyHttpRequestBuilder
from integration_tests.http.mhs_http_request_builder import MhsHttpRequestBuilder
from integration_tests.xml.eb_xml_assertor import EbXmlResponseAssertor


class ForwardReliablesMessagingPatternTests(unittest.TestCase):
    """
    These tests show a forward-reliable response from Spine via the MHS for the example message interaction
    of Common Content Forward Reliable GP2GP Large Message Attachment.

    They make use of the fake-spine service, which has known responses for certain message ids.
    They make use of the fake-spine-route-lookup service, which has known responses for certain interaction ids.
    """

    RETRY_MESSAGE_ID = "35586865-45B0-41A5-98F6-817CA6F1F5EF"
    SOAP_FAULT_MESSAGE_ID = "3771F30C-A231-4D64-A46C-E7FB0D52C27C"
    EBXML_FAULT_MESSAGE_ID = "A7D43B03-38FB-4ED7-8D04-0496DBDEDB7D"

    COPC_INTERACTION = "COPC_IN000001UK01"
    PRSC_INTERACTION = "PRSC_IN080000UK07"

    DEFAULT_PARTY_ID = "9689177923"
    SOAP_ERROR_PARTY_ID = "9446245796"

    def setUp(self):
        MHS_STATE_TABLE_WRAPPER.clear_all_records_in_table()
        MHS_SYNC_ASYNC_TABLE_WRAPPER.clear_all_records_in_table()
        MHS_INBOUND_QUEUE.drain()

    def _build_copc_message(self, party_id=None, message_id=None, **kwargs):
        return build_message(
            self.COPC_INTERACTION,
            party_id or self.DEFAULT_PARTY_ID,
            message_id=message_id,
            **kwargs
        )

    def _post_to_inbound_proxy(self, message, expect_success=True):
        builder = InboundProxyHttpRequestBuilder().with_body(message)
        return (
            builder.execute_post_expecting_success()
            if expect_success
            else builder.execute_post_expecting_error_response()
        )

    def _post_to_mhs(
            self,
            interaction_id,
            message_id,
            message,
            wait_for_response=False,
            expect="success",
            attachments=None,
    ):
        builder = (
            MhsHttpRequestBuilder()
            .with_headers(
                interaction_id=interaction_id,
                message_id=message_id,
                wait_for_response=wait_for_response,
            )
            .with_body(message, attachments=attachments)
        )

        if expect == "success":
            return builder.execute_post_expecting_success()
        if expect == "error":
            return builder.execute_post_expecting_error_response()
        if expect == "bad_request":
            return builder.execute_post_expecting_bad_request_response()

        raise ValueError(f"Unknown expect type: {expect}")

    def _assert_table_state(self, message_id, outbound_status, workflow):
        MhsTableStateAssertor(
            MHS_STATE_TABLE_WRAPPER.get_all_records_in_table()
        ).assert_single_item_exists_with_key(message_id).assert_item_contains_values(
            {
                "INBOUND_STATUS": None,
                "OUTBOUND_STATUS": outbound_status,
                "WORKFLOW": workflow,
            }
        )

    def test_should_place_unsolicited_valid_message_onto_queue_for_client_to_receive(self):
        message, message_id = build_message(
            "INBOUND_UNEXPECTED_MESSAGE",
            self.DEFAULT_PARTY_ID,
            to_party_id="test-party-key",
        )

        self._post_to_inbound_proxy(message)

        AMQMessageAssertor(MHS_INBOUND_QUEUE.get_next_message_on_queue()) \
            .assert_property("message-id", message_id) \
            .assert_durable_is(True) \
            .assertor_for_hl7_xml_message() \
            .assert_element_attribute(
            ".//ControlActEvent//code",
            "displayName",
            "GP2GP Large Message Attachment Information",
        )

    def test_should_return_nack_when_forward_reliable_message_is_not_meant_for_the_mhs_system(self):
        message, _ = build_message(
            "INBOUND_UNEXPECTED_MESSAGE",
            self.DEFAULT_PARTY_ID,
            to_party_id="NOT_THE_MHS",
        )

        response = self._post_to_inbound_proxy(message)

        EbXmlResponseAssertor(response.text) \
            .assert_element_attribute(".//ErrorList//Error", "errorCode", "ValueNotRecognized") \
            .assert_element_attribute(".//ErrorList//Error", "severity", "Error") \
            .assert_element_exists_with_value(
            ".//ErrorList//Error//Description",
            "501314:Invalid To Party Type attribute",
        )

    def test_should_return_500_response_when_inbound_service_receives_message_in_invalid_format(self):
        message, _ = build_message("INBOUND_UNEXPECTED_INVALID_MESSAGE", self.DEFAULT_PARTY_ID)

        response = self._post_to_inbound_proxy(message, expect_success=False)

        self.assertIn("Exception during inbound message parsing", response.text)

    def test_should_return_successful_response_to_client_when_a_business_level_retry_is_required_and_succeeds(self):
        """
        Message ID: '35586865-45B0-41A5-98F6-817CA6F1F5EF' configured in fakespine to return a SOAP Fault error,
        after 2 retries fakespine will return a success response.
        """

        message, message_id = self._build_copc_message(
            message_id=self.RETRY_MESSAGE_ID
        )

        self._post_to_mhs(
            self.COPC_INTERACTION,
            message_id,
            message,
            wait_for_response=False,
            expect="success",
        )

    def test_should_record_message_status_when_a_business_level_retry_is_required_and_succeeds(self):
        """
        Message ID: '35586865-45B0-41A5-98F6-817CA6F1F5EF' configured in fakespine to return a SOAP Fault error,
        after 2 retries fakespine will return a success response.
        """

        message, message_id = self._build_copc_message(
            message_id=self.RETRY_MESSAGE_ID
        )

        self._post_to_mhs(
            self.COPC_INTERACTION,
            message_id,
            message,
            wait_for_response=False,
            expect="success",
        )

        self._assert_table_state(
            message_id,
            "OUTBOUND_MESSAGE_ACKD",
            "forward-reliable",
        )

    def test_should_return_information_from_soap_fault_returned_by_spine_in_original_post_request_to_client(self):
        """
        Message ID: 3771F30C-A231-4D64-A46C-E7FB0D52C27C configured in fakespine to return a SOAP Fault error.
        Error found here: fake_spine/fake_spine/configured_responses/soap_fault_single_error.xml
        """

        message, message_id = self._build_copc_message(
            party_id=self.SOAP_ERROR_PARTY_ID,
            message_id=self.SOAP_FAULT_MESSAGE_ID,
        )

        response = self._post_to_mhs(
            self.COPC_INTERACTION,
            message_id,
            message,
            wait_for_response=False,
            expect="error",
        )

        JsonErrorResponseAssertor(response.text) \
            .assert_error_code(200) \
            .assert_code_context("urn:nhs:names:error:tms") \
            .assert_severity("Error")

    def test_should_record_message_status_when_soap_fault_returned_from_spine(self):
        """
        Message ID: 3771F30C-A231-4D64-A46C-E7FB0D52C27C configured in fakespine to return a SOAP Fault error.
        Error found here: fake_spine/fake_spine/configured_responses/soap_fault_single_error.xml
        """

        message, message_id = self._build_copc_message(
            party_id=self.SOAP_ERROR_PARTY_ID,
            message_id=self.SOAP_FAULT_MESSAGE_ID,
        )

        self._post_to_mhs(
            self.COPC_INTERACTION,
            message_id,
            message,
            wait_for_response=False,
            expect="error",
        )

        self._assert_table_state(
            message_id,
            "OUTBOUND_MESSAGE_NACKD",
            "forward-reliable",
        )

    def test_should_return_bad_request_when_client_sends_invalid_message(self):
        message, message_id = self._build_copc_message()

        attachments = [
            {
                "content_type": "application/zip",
                "is_base64": False,
                "description": "Some description",
                "payload": "Some payload",
            }
        ]

        response = self._post_to_mhs(
            self.COPC_INTERACTION,
            message_id,
            message,
            wait_for_response=False,
            expect="bad_request",
            attachments=attachments,
        )

        self.assertEqual(
            response.text,
            "400: Invalid request. Validation errors: {'attachments': {0: "
            "{'content_type': ['Must be one of: text/plain, text/html, application/pdf, "
            "text/xml, application/xml, text/rtf, audio/basic, audio/mpeg, image/png, "
            "image/gif, image/jpeg, image/tiff, video/mpeg, application/msword, "
            "application/octet-stream.']}}}"
        )
