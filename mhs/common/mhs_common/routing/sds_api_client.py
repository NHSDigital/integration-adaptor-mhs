import json
import urllib.parse
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
    async def get_end_point(self, interaction_id: str, ods_code: str = None) -> Dict:
        endpoint_resource = await self._get_endpoint_resource(interaction_id, ods_code)

        result = {
            "nhsMhsFQDN": self._get_identifier_value(endpoint_resource, "https://fhir.nhs.uk/Id/nhsMhsFQDN"),
            "nhsMHSEndPoint": [
                endpoint_resource['address']
            ],
            "nhsMHSPartyKey": self._get_identifier_value(endpoint_resource, "https://fhir.nhs.uk/Id/nhsMhsPartyKey"),
            "nhsMhsCPAId": self._get_identifier_value(endpoint_resource, "https://fhir.nhs.uk/Id/nhsMhsCPAId"),
            "uniqueIdentifier": [
                self._get_identifier_value(endpoint_resource, "https://fhir.nhs.uk/Id/nhsMHSId")
            ]
        }
        return result

    @timing.time_function
    async def get_reliability(self, interaction_id: str, ods_code: str = None) -> Dict:
        endpoint_resource = await self._get_endpoint_resource(interaction_id, ods_code)

        result = {
            "nhsMHSSyncReplyMode": self._get_extension(endpoint_resource, 'nhsMHSSyncReplyMode', 'valueString'),
            "nhsMHSRetryInterval": self._get_extension(endpoint_resource, 'nhsMHSRetryInterval', 'valueString'),
            "nhsMHSRetries": self._get_extension(endpoint_resource, 'nhsMHSRetries', 'valueInteger'),
            "nhsMHSPersistDuration": self._get_extension(endpoint_resource, 'nhsMHSPersistDuration', 'valueString'),
            "nhsMHSDuplicateElimination": self._get_extension(endpoint_resource, 'nhsMHSDuplicateElimination', 'valueString'),
            "nhsMHSAckRequested": self._get_extension(endpoint_resource, 'nhsMHSAckRequested', 'valueString')
        }
        return result

    def _build_headers(self):
        tracking_headers = build_tracking_headers()
        headers = {
            'X-Correlation-ID': tracking_headers[HttpHeaders.CORRELATION_ID],
            'apikey': self.api_key
        }

        return headers

    @staticmethod
    def _build_organization_query_param(organization):
        return urllib.parse.quote(f'https://fhir.nhs.uk/Id/ods-organization-code|{organization}')

    @staticmethod
    def _build_interaction_query_param(interaction):
        return urllib.parse.quote(f'https://fhir.nhs.uk/Id/nhsServiceInteractionId|{interaction}')

    @staticmethod
    def _build_partykey_query_param(partykey):
        return urllib.parse.quote(f'https://fhir.nhs.uk/Id/nhsMhsPartyKey|{partykey}')

    def _build_endpoint_url(self, interaction, partykey):
        interaction = self._build_interaction_query_param(interaction)
        partykey = self._build_partykey_query_param(partykey)
        return f"{self.base_url}/Endpoint?identifier={interaction}&identifier={partykey}"

    def _build_device_url(self, organization, interaction):
        organization = self._build_organization_query_param(organization)
        interaction = self._build_interaction_query_param(interaction)
        return f"{self.base_url}/Device?organization={organization}&identifier={interaction}"

    @staticmethod
    def _get_identifier_value(resource, system):
        return list(filter(lambda kv: kv['system'] == system, resource['identifier']))[0]['value']

    @staticmethod
    def _set_identifier_value(resource, system, value):
        list(filter(lambda kv: kv['system'] == system, resource['identifier']))[0]['value'] = value

    @staticmethod
    def _get_extension(endpoint, system, value_key):
        def _get_extensions(resource):
            return list(filter(lambda kv: kv['url'] == 'https://fhir.nhs.uk/StructureDefinition/Extension-SDS-ReliabilityConfiguration', resource['extension']))[0]['extension']
        extensions_matching_system = list(filter(lambda kv: kv['url'] == system, _get_extensions(endpoint)))
        if len(extensions_matching_system) > 0:
            return extensions_matching_system[0][value_key]
        return None

    async def _get_endpoint_resource(self, interaction_id: str, ods_code: str = None) -> Dict:
        if not ods_code:
            logger.info("No org code provided when obtaining endpoint details. Using {spine_org_code}",
                        fparams={"spine_org_code": ods_code})
            ods_code = self.spine_org_code

        device_resource = await self._get_sds_device_resource(interaction_id, ods_code)

        party_key = self._get_identifier_value(device_resource, 'https://fhir.nhs.uk/Id/nhsMhsPartyKey')

        endpoint_resource = await self._get_sds_endpoint_resource(interaction_id, party_key)

        # copy asid from Device to Endpoint the same as SpineRouteLookup does
        asid = self._get_identifier_value(device_resource, 'https://fhir.nhs.uk/Id/nhsSpineASID')
        self._set_identifier_value(endpoint_resource, "https://fhir.nhs.uk/Id/nhsMHSId", asid)

        return endpoint_resource

    async def _get_sds_device_resource(self, interaction_id: str, ods_code: str) -> Dict:
        device_url = self._build_device_url(ods_code, interaction_id)

        # If 599 error is encountered, ensure your env var path points to the correct cert,
        # such as: CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
        http_response = await common_https.CommonHttps.make_request(url=device_url, method="GET", headers=self._build_headers(), body=None)
        device_result = json.loads(http_response.body.decode())
        resources = list(map(lambda kv: kv['resource'], device_result['entry'])) if 'entry' in device_result else []

        if len(resources) == 0:
            raise SDSException('Empty response for /Device')
        if len(resources) > 1:
            logger.warning("More than one resource returned for /Device call:: {ods_code} & "
                           "{interaction_id}", fparams={"ods_code": ods_code, "interaction_id": interaction_id})

        return resources[0]

    async def _get_sds_endpoint_resource(self, interaction_id: str, party_key: str) -> Dict:
        endpoint_url = self._build_endpoint_url(interaction_id, party_key)

        http_response = await common_https.CommonHttps.make_request(url=endpoint_url, method="GET", headers=self._build_headers(), body=None)
        sds_api_result = json.loads(http_response.body.decode())

        if 'resourceType' not in sds_api_result or sds_api_result['resourceType'] != 'Bundle':
            raise SDSException('Unexpected SDS API response: ', str(http_response))

        resources = list(map(lambda kv: kv['resource'], sds_api_result['entry'])) if 'entry' in sds_api_result else []

        if len(resources) == 0:
            raise SDSException('Empty response from accredited system lookup')
        if len(resources) > 1:
            logger.warning("More than one accredited system details returned on inputs: {interaction_id} & "
                           "{party_key}", fparams={"interaction_id": interaction_id, "party_key": party_key})

        return resources[0]
