import json
import os
import unittest
from pathlib import Path
from unittest import mock

from tornado import httpclient

from mhs_common.routing.exceptions import SDSException
from utilities import test_utilities, mdc

from mhs_common.routing import sds_api_client

TEST_DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / 'data'


def load_test_data(file_name):
    with open(f'{TEST_DATA_DIR}/{file_name}', 'r') as f:
        return f.read()


BASE_URL = "https://example.com"
API_KEY = "API_KEY"
ROUTING_PATH = "Endpoint"
RELIABILITY_PATH = "Endpoint"
SPINE_ORG_CODE = "SPINE_ORG_CODE"
HTTP_METHOD = "GET"
ORG_CODE = "ORG_CODE"
SERVICE_ID = "SERVICE_ID"
JSON_RESPONSE = load_test_data('sds_response.json').encode()
JSON_ZERO_RESULTS_RESPONSE = load_test_data('sds_zero_results_response.json').encode()
JSON_MULTIPLE_RESULTS_RESPONSE = load_test_data('sds_multiple_results_response.json').encode()
JSON_UNEXPECTED_RESPONSE = load_test_data('sds_unexpected_response.json').encode()
EXPECTED_ROUTING = json.loads(load_test_data('routing.json'))
EXPECTED_RELIABILITY = json.loads(load_test_data('reliability.json'))
CORRELATION_ID = 'CORRELATION_ID'


class TestSdsApiClient(unittest.TestCase):

    def setUp(self) -> None:
        # Mock the httpclient.AsyncHTTPClient() constructor
        patcher = unittest.mock.patch.object(httpclient, "AsyncHTTPClient")
        mock_http_client_constructor = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock the AsyncHTTPClient client class itself
        self.mock_http_client = unittest.mock.MagicMock()
        mock_http_client_constructor.return_value = self.mock_http_client

        mdc.correlation_id.set(CORRELATION_ID)

    def tearDown(self) -> None:
        mdc.correlation_id.set(None)

    @test_utilities.async_test
    async def test_should_retrieve_routing_and_reliability_details_if_given_org_code(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        for function_to_test, expected_result in [(self.routing.get_end_point, EXPECTED_ROUTING), (self.routing.get_reliability, EXPECTED_RELIABILITY)]:
            with self.subTest(function_to_test.__name__):
                self._given_http_client_returns_a_json_response(JSON_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID, ORG_CODE)

                self.assertEqual(expected_result, routing_details)
                expected_url = self._build_url(path=ROUTING_PATH)
                self._assert_http_client_called_with_expected_args(expected_url)

    @test_utilities.async_test
    async def test_should_retrieve_routing_and_reliability_details_if_given_no_org_code(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        for function_to_test, expected_result in [(self.routing.get_end_point, EXPECTED_ROUTING), (self.routing.get_reliability, EXPECTED_RELIABILITY)]:
            with self.subTest(function_to_test.__name__):
                self._given_http_client_returns_a_json_response(JSON_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID)

                self.assertEqual(expected_result, routing_details)
                expected_url = self._build_url(path=ROUTING_PATH, org_code=SPINE_ORG_CODE)
                self._assert_http_client_called_with_expected_args(expected_url)

    @test_utilities.async_test
    async def test_should_retrieve_routing_and_reliability_first_endpoint_details_if_there_are_multiple_results(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        for function_to_test, expected_result in [(self.routing.get_end_point, EXPECTED_ROUTING), (self.routing.get_reliability, EXPECTED_RELIABILITY)]:
            with self.subTest(function_to_test.__name__):
                self._given_http_client_returns_a_json_response(JSON_MULTIPLE_RESULTS_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID)

                self.assertEqual(expected_result, routing_details)
                expected_url = self._build_url(path=ROUTING_PATH, org_code=SPINE_ORG_CODE)
                self._assert_http_client_called_with_expected_args(expected_url)

    @test_utilities.async_test
    async def test_should_raise_error_if_endpoint_yields_no_result(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        self._given_http_client_returns_a_json_response(JSON_ZERO_RESULTS_RESPONSE)

        for function_to_test in [self.routing.get_end_point, self.routing.get_reliability]:
            with self.subTest(function_to_test.__name__):
                with self.assertRaises(SDSException):
                    await function_to_test(SERVICE_ID, ORG_CODE)

    @test_utilities.async_test
    async def test_should_raise_error_if_endpoint_returns_unexpected_response(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        self._given_http_client_returns_a_json_response(JSON_UNEXPECTED_RESPONSE)

        for function_to_test in [self.routing.get_end_point, self.routing.get_reliability]:
            with self.subTest(function_to_test.__name__):
                with self.assertRaises(SDSException):
                    await self.routing.get_end_point(SERVICE_ID, ORG_CODE)

    def _given_http_client_returns_a_json_response(self, response):
        mock_response = mock.Mock()
        mock_response.body = response
        self.mock_http_client.fetch.return_value = test_utilities.awaitable(mock_response)

    def _assert_http_client_called_with_expected_args(self, expected_url, client_cert=None, client_key=None, ca_certs=None, proxy_host=None, proxy_port=None):
        self.mock_http_client.fetch.assert_called_with(expected_url, raise_error=True,
                                                       method=HTTP_METHOD, body=None,
                                                       headers={'X-Correlation-ID': CORRELATION_ID, 'apikey': API_KEY},
                                                       client_cert=client_cert, client_key=client_key,
                                                       ca_certs=ca_certs, validate_cert=True, proxy_host=proxy_host,
                                                       proxy_port=proxy_port)

    @staticmethod
    def _build_url(path: str, org_code: str = ORG_CODE) -> str:
        return f'{BASE_URL}/{path}?organization=https://fhir.nhs.uk/Id/ods-organization-code|{org_code}&identifier=https://fhir.nhs.uk/Id/nhsServiceInteractionId|{SERVICE_ID}'