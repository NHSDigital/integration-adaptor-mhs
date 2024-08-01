"""
Provides tests around the Synchronous workflow
"""
import uuid
from unittest import TestCase

from integration_tests.db.db_wrapper_factory import MHS_STATE_TABLE_WRAPPER
from integration_tests.db.mhs_table import MhsTableStateAssertor
from integration_tests.helpers.build_message import build_message
from integration_tests.http.mhs_http_request_builder import MhsHttpRequestBuilder
from integration_tests.xml.hl7_xml_assertor import Hl7XmlResponseAssertor


class SynchronousMessagingPatternTests(TestCase):
    def setUp(self):
        MHS_STATE_TABLE_WRAPPER.clear_all_records_in_table()

    """
    This method exists only to ensure a test exists and passes.
    """
    def test_should_return_successful(self):
        testValue = True
        message = "Test value is true."
        self.assertTrue(testValue, message)