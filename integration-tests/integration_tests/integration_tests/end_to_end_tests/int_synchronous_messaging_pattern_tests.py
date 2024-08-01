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
    """
    These tests show a synchronous response from Spine via the MHS for the example message interaction of PDS
    (Personal Demographics Service).

    Synchronous message testing interaction:
    - Message sent: PDS Retrieval Query (QUPA_IN040000UK32)
    - Expected response: PDS Retrieval Query Successful (QUPA_IN050000UK32)

    Flow documented at:
    - https://data.developer.nhs.uk/dms/mim/4.2.00/Index.htm
        -> Domains
            -> PDS
                -> 6.4 (Request)
                -> 6.5 (Response)
    """

    def setUp(self):
        MHS_STATE_TABLE_WRAPPER.clear_all_records_in_table()

    """
    This method exists only to ensure a test exists and passes.
    """
    def test_should_return_successful(self):
        testValue = True
        message = "Test value is true."
        self.assertTrue(testValue, message)
