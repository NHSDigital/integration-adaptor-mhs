from unittest import TestCase
from utilities import file_utilities
import certifi
import definitions
import handlers
import json
import os
import pathlib

complete_data_path = pathlib.Path(definitions.ROOT_DIR) / 'tests' / 'data' / 'complete_input.json'


def get_target_address():
    return os.getenv('SCR_SERVICE_ADDRESS', 'http://localhost')


class SCREndpointTest(TestCase):

    def test_scr_happy_path(self):
        body = file_utilities.get_file_dict(complete_data_path)
        response = handlers.post(f"{get_target_address()}/gp_summary_upload",
                                 data=json.dumps(body), verify=certifi.where())
        self.assertEqual(json.dumps(json.loads(response.text)), json.dumps(body))
