import json
from typing import Dict

from comms import common_https
from comms.http_headers import HttpHeaders
from mhs_common.routing.exceptions import SDSException
from mhs_common.routing.route_lookup_client import RouteLookupClient
from utilities.mdc import build_tracking_headers
from utilities import integration_adaptors_logger as log, timing

logger = log.IntegrationAdaptorsLogger(__name__)


class SdsApiClient(RouteLookupClient):

    def __init__(self, base_url, api_key, spine_org_code) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.spine_org_code = spine_org_code

    @timing.time_function
    async def get_end_point(self, service_id: str, org_code: str = None) -> Dict:
        resource = await self._get_endpoint_resource(service_id, org_code)

        identifier = resource['identifier']

        def get_identifier_value(system):
            return list(filter(lambda kv: kv['system'] == system, identifier))[0]['value']

        result = {
            "nhsMhsFQDN": get_identifier_value("https://fhir.nhs.uk/Id/nhsMhsFQDN"),
            "nhsMHSEndPoint": [
                resource['address']
            ],
            "nhsMHSPartyKey": get_identifier_value("https://fhir.nhs.uk/Id/nhsMhsPartyKey"),
            "nhsMhsCPAId": get_identifier_value("https://fhir.nhs.uk/Id/nhsMhsCPAId"),
            "uniqueIdentifier": [
                get_identifier_value("https://fhir.nhs.uk/Id/nhsMHSId")
            ]
        }
        return result

    @timing.time_function
    async def get_reliability(self, service_id: str, org_code: str = None) -> Dict:
        resource = await self._get_endpoint_resource(service_id, org_code)

        extensions = list(filter(lambda kv: kv['url'] == 'https://fhir.nhs.uk/StructureDefinition/Extension-SDS-ReliabilityConfiguration', resource['extension']))[0]['extension']

        def get_extension(system, value_key):
            return list(filter(lambda kv: kv['url'] == system, extensions))[0][value_key]

        result = {
            "nhsMHSSyncReplyMode": get_extension('nhsMHSSyncReplyMode', 'valueString'),
            "nhsMHSRetryInterval": get_extension('nhsMHSRetryInterval', 'valueString'),
            "nhsMHSRetries": get_extension('nhsMHSRetries', 'valueInteger'),
            "nhsMHSPersistDuration": get_extension('nhsMHSPersistDuration', 'valueString'),
            "nhsMHSDuplicateElimination": get_extension('nhsMHSDuplicateElimination', 'valueString'),
            "nhsMHSAckRequested": get_extension('nhsMHSAckRequested', 'valueString')
        }
        return result

    def _build_headers(self):
        tracking_headers = build_tracking_headers()
        headers = {
            'X-Correlation-ID': tracking_headers[HttpHeaders.CORRELATION_ID],
            'apikey': self.api_key
        }

        return headers

    async def _get_endpoint_resource(self, service_id: str, org_code: str = None) -> Dict:
        if not org_code:
            logger.info("No org code provided when obtaining endpoint details. Using {spine_org_code}",
                        fparams={"spine_org_code": org_code})
            org_code = self.spine_org_code

        url = f"{self.base_url}/Endpoint?organization=https://fhir.nhs.uk/Id/ods-organization-code|{org_code}&identifier=https://fhir.nhs.uk/Id/nhsServiceInteractionId|{service_id}"

        http_response = await common_https.CommonHttps.make_request(url=url, method="GET", headers=self._build_headers(), body=None)
        sds_api_result = json.loads(http_response.body.decode())

        if 'resourceType' not in sds_api_result or sds_api_result['resourceType'] != 'Bundle':
            raise SDSException('Unexpected SDS API response: ', str(http_response))

        resources = list(map(lambda kv: kv['resource'], sds_api_result['entry'])) if 'entry' in sds_api_result else []

        if len(resources) == 0:
            raise SDSException('No response from accredited system lookup')
        if len(resources) > 1:
            logger.warning("More than one accredited system details returned on inputs: {ods_code} & "
                           "{interaction_id}", fparams={"ods_code": org_code, "interaction_id": service_id})

        return resources[0]
