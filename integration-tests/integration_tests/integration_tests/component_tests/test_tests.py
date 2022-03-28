"""Component tests related to the asynchronous-express message pattern"""

import unittest
import requests

class TestTest(unittest.TestCase):
    
    def test_test1(self):
        response = requests.get('http://localhost:8080/__admin/mappings')
        body = response.json()
        print(response)

    def test_test2(self):
        response = requests.get('http://sds-api-mock:8080/__admin/mappings')
        body = response.json()
        print(response)

