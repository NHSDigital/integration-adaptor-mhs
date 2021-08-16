import unittest
import requests


class SdsApiMockTests(unittest.TestCase):
    def test_sds_api_mock_8080(self):
        response = requests.get('http://sds-api-mock:8080/__admin/mappings')
        print(response.json())

    def test_sds_api_mock_8081(self):
        response = requests.get('http://sds-api-mock:8081/__admin/mappings')
        print(response.json())