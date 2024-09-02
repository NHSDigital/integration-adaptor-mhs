import json
import os
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock
from unittest.mock import call

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
ENDPOINT_PATH = "Endpoint"
DEVICE_PATH = "Device"
SPINE_ORG_CODE = "SPINE_ORG_CODE"
OWNER_ORG_CODE = "OWNER_ORG_CODE"
HTTP_METHOD = "GET"
ORG_CODE = "ORG_CODE"
SERVICE_ID = "SERVICE_ID"
PARTY_KEY = "PARTY_KEY"
SDS_DEVICE_JSON_RESPONSE = load_test_data('sds_device_response.json').encode()
SDS_DEVICE_JSON_MULTIPLE_RESULTS_RESPONSE = load_test_data('sds_device_multiple_results_response.json').encode()
SDS_ENDPOINT_JSON_RESPONSE = load_test_data('sds_endpoint_response.json').encode()
SDS_ENDPOINT_JSON_MULTIPLE_RESULTS_RESPONSE = load_test_data('sds_endpoint_multiple_results_response.json').encode()
SDS_JSON_ZERO_RESULTS_RESPONSE = load_test_data('sds_zero_results_response.json').encode()
SDS_JSON_UNEXPECTED_RESPONSE = load_test_data('sds_unexpected_response.json').encode()
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
                self._given_http_client_returns_a_json_response(SDS_DEVICE_JSON_RESPONSE, SDS_ENDPOINT_JSON_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID, ORG_CODE)

                self.assertEqual(expected_result, routing_details)

                expected_device_url = self._build_url(path=DEVICE_PATH, org_code=ORG_CODE, interaction_id=SERVICE_ID)
                expected_endpoint_url = self._build_url(path=ENDPOINT_PATH, interaction_id=SERVICE_ID, party_key=PARTY_KEY)

                self._assert_http_client_called_with_expected_args([expected_device_url, expected_endpoint_url])


    @test_utilities.async_test
    async def test_should_retrieve_routing_and_reliability_details_if_given_no_org_code(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        for function_to_test, expected_result in [(self.routing.get_end_point, EXPECTED_ROUTING), (self.routing.get_reliability, EXPECTED_RELIABILITY)]:
            with self.subTest(function_to_test.__name__):
                self._given_http_client_returns_a_json_response(SDS_DEVICE_JSON_RESPONSE, SDS_ENDPOINT_JSON_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID)

                self.assertEqual(expected_result, routing_details)

                expected_device_url = self._build_url(path=DEVICE_PATH, org_code=SPINE_ORG_CODE, interaction_id=SERVICE_ID)
                expected_endpoint_url = self._build_url(path=ENDPOINT_PATH, interaction_id=SERVICE_ID, party_key=PARTY_KEY)

                self._assert_http_client_called_with_expected_args([expected_device_url, expected_endpoint_url])

    @test_utilities.async_test
    async def test_should_retrieve_routing_and_reliability_first_endpoint_details_if_there_are_multiple_results(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        for function_to_test, expected_result in [(self.routing.get_end_point, EXPECTED_ROUTING), (self.routing.get_reliability, EXPECTED_RELIABILITY)]:
            with self.subTest(function_to_test.__name__):
                self._given_http_client_returns_a_json_response(SDS_DEVICE_JSON_MULTIPLE_RESULTS_RESPONSE, SDS_ENDPOINT_JSON_MULTIPLE_RESULTS_RESPONSE)

                routing_details = await function_to_test(SERVICE_ID)

                self.assertEqual(expected_result, routing_details)

                expected_device_url = self._build_url(path=DEVICE_PATH, org_code=SPINE_ORG_CODE, interaction_id=SERVICE_ID)
                expected_endpoint_url = self._build_url(path=ENDPOINT_PATH, interaction_id=SERVICE_ID, party_key=PARTY_KEY)

                self._assert_http_client_called_with_expected_args([expected_device_url, expected_endpoint_url])

    @test_utilities.async_test
    async def test_should_raise_error_if_endpoint_yields_no_result(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        self._given_http_client_returns_a_json_response(SDS_JSON_ZERO_RESULTS_RESPONSE, SDS_JSON_ZERO_RESULTS_RESPONSE)

        for function_to_test in [self.routing.get_end_point, self.routing.get_reliability]:
            with self.subTest(function_to_test.__name__):
                with self.assertRaises(SDSException):
                    await function_to_test(SERVICE_ID, ORG_CODE)

    @test_utilities.async_test
    async def test_should_raise_error_if_endpoint_returns_unexpected_response(self):
        self.routing = sds_api_client.SdsApiClient(BASE_URL, API_KEY, SPINE_ORG_CODE)
        self._given_http_client_returns_a_json_response(SDS_JSON_UNEXPECTED_RESPONSE, SDS_JSON_UNEXPECTED_RESPONSE)

        for function_to_test in [self.routing.get_end_point, self.routing.get_reliability]:
            with self.subTest(function_to_test.__name__):
                with self.assertRaises(SDSException):
                    await self.routing.get_end_point(SERVICE_ID, ORG_CODE)

    def _given_http_client_returns_a_json_response(self, device_response, endpoint_response):
        mock_device_response = mock.Mock()
        mock_device_response.body = device_response
        mock_endpoint_response = mock.Mock()
        mock_endpoint_response.body = endpoint_response
        self.mock_http_client.fetch.side_effect = [
            test_utilities.awaitable(mock_device_response),
            test_utilities.awaitable(mock_endpoint_response)
        ]

    def _assert_http_client_called_with_expected_args(self, expected_urls):
        expected_urls = expected_urls if type(expected_urls) == list else [expected_urls]

        calls = [call(expected_url, raise_error=True,
                      method=HTTP_METHOD, body=None,
                      headers={'X-Correlation-ID': CORRELATION_ID, 'apikey': API_KEY},
                      client_cert=None, client_key=None,
                      ca_certs='/etc/pki/tls/certs/ca-certificates.crt', validate_cert=True, proxy_host=None,
                      proxy_port=None)
                 for expected_url in expected_urls]

        self.mock_http_client.fetch.assert_has_calls(calls)

    @staticmethod
    def _build_url(path: str, org_code: str = None, interaction_id: str = None, party_key: str = None) -> str:
        query_params = [
            ('organization', 'https://fhir.nhs.uk/Id/ods-organization-code', org_code),
            ('identifier', 'https://fhir.nhs.uk/Id/nhsServiceInteractionId', interaction_id),
            ('identifier', 'https://fhir.nhs.uk/Id/nhsMhsPartyKey', party_key),
        ]

        query_params = "&".join(map(lambda v: f'{v[0]}={urllib.parse.quote(f"{v[1]}|{v[2]}")}', filter(lambda v: v[2], query_params)))

        return f'{BASE_URL}/{path}?{query_params}'
