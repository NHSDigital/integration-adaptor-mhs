from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock

from tornado import httpclient

from comms.common_https import CommonHttps
from utilities.test_utilities import awaitable
from unittest.mock import ANY

URL = "ABC.ABC"
METHOD = "GET"
HEADERS = {"a": "1"}
BODY = "hello"
CLIENT_CERT = "client.cert"
CLIENT_KEY = "client.key"
CA_CERTS = "ca.certs"
HTTP_PROXY_HOST = "http_proxy"
HTTP_PROXY_PORT = 3128


class TestCommonHttps(IsolatedAsyncioTestCase):

    async def test_make_request(self):
        with patch.object(httpclient.AsyncHTTPClient(), "fetch") as mock_fetch:
            return_value = Mock()
            mock_fetch.return_value = awaitable(return_value)

            actual_response = await CommonHttps.make_request(url=URL, method=METHOD, headers=HEADERS, body=BODY,
                                                             client_cert=CLIENT_CERT, client_key=CLIENT_KEY,
                                                             ca_certs=CA_CERTS, validate_cert=False,
                                                             http_proxy_host=HTTP_PROXY_HOST,
                                                             http_proxy_port=HTTP_PROXY_PORT)

            mock_fetch.assert_called_with(URL,
                                          raise_error=True,
                                          method=METHOD,
                                          body=BODY,
                                          headers=HEADERS,
                                          client_cert=CLIENT_CERT,
                                          client_key=CLIENT_KEY,
                                          ca_certs=CA_CERTS,
                                          validate_cert=False,
                                          proxy_host=HTTP_PROXY_HOST,
                                          proxy_port=HTTP_PROXY_PORT)

            self.assertIs(actual_response, return_value, "Expected content should be returned.")

    async def test_make_request_defaults(self):
        with patch.object(httpclient.AsyncHTTPClient(), "fetch") as mock_fetch:
            return_value = Mock()
            mock_fetch.return_value = awaitable(return_value)

            actual_response = await CommonHttps.make_request(url=URL, method=METHOD, headers=HEADERS, body=BODY)

            mock_fetch.assert_called_with(URL,
                                          raise_error=True,
                                          method=METHOD,
                                          body=BODY,
                                          headers=HEADERS,
                                          client_cert=None,
                                          client_key=None,
                                          ca_certs=ANY,
                                          validate_cert=True,
                                          proxy_host=None,
                                          proxy_port=None)

            self.assertIs(actual_response, return_value, "Expected content should be returned.")

    async def test_make_request_with_no_cacert_uses_ssl_default_verify_path_cafile(self):
        import ssl
        with patch.object(httpclient.AsyncHTTPClient(), "fetch") as mock_fetch, \
            patch.object(ssl, 'get_default_verify_paths', return_value=ssl.DefaultVerifyPaths(
                CA_CERTS, None, None, None, None, None
            )):
            return_value = Mock()
            mock_fetch.return_value = awaitable(return_value)

            actual_response = await CommonHttps.make_request(url=URL, method=METHOD, headers=HEADERS, body=BODY,
                                                             client_cert=CLIENT_CERT, client_key=CLIENT_KEY,
                                                             ca_certs=None, validate_cert=False,
                                                             http_proxy_host=HTTP_PROXY_HOST,
                                                             http_proxy_port=HTTP_PROXY_PORT)

            mock_fetch.assert_called_with(URL,
                                          raise_error=True,
                                          method=METHOD,
                                          body=BODY,
                                          headers=HEADERS,
                                          client_cert=CLIENT_CERT,
                                          client_key=CLIENT_KEY,
                                          ca_certs=CA_CERTS,
                                          validate_cert=False,
                                          proxy_host=HTTP_PROXY_HOST,
                                          proxy_port=HTTP_PROXY_PORT)

            self.assertIs(actual_response, return_value, "Expected content should be returned.")
