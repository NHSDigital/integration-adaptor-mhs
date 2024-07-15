"""A script that checks that AWS load balancers have all healthy targets. For use in CI builds."""

import argparse
import certifi
import requests
import sys
import urllib3
from typing import List

import boto3


def main(target_group_arns: List[str]):
    client = boto3.client('elbv2')

    for target_group_arn in target_group_arns:
        response = client.describe_target_health(TargetGroupArn=target_group_arn)
        for target_health_description in response['TargetHealthDescriptions']:
            if target_health_description['TargetHealth']['State'] != 'healthy':
                sys.exit(1)


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Check AWS load balancer target groups have all healthy targets")

    parser.add_argument("target_group_arns", nargs = '+', help="The ARNs of the target groups to check")

    return parser.parse_args()


def _check_services_healthchecks():
    print('Checking all services healthchecks')

    protocols = ['http', 'https']
    base_url = '{protocol}://mhs-{service}.build.nhsredteam.internal.nhs.uk/healthcheck'

    for protocol, service in [(protocol, service) for service in ['outbound', 'inbound', 'route'] for protocol in protocols]:
        url = base_url.format(protocol=protocol, service=service)
        print('Checking: ' + url)
        try:
            response = requests.get(url, verify=False, timeout=5)
            print('{service}: {status_code}'.format(service=service, status_code=str(response.status_code)))
        except Exception as ex:
            print(ex)


def _send_outbound_post():
    print('Checking outbound post request')

    urls = [
        'https://mhs-outbound.build.nhsredteam.internal.nhs.uk/',
        'https://mhs-outbound.build.nhsredteam.internal.nhs.uk',
    ]
    
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    headers = {
        'Interaction-Id': 'test',
        'Message-Id': 'test',
        'Correlation-Id': 'test',
        'wait-for-response': 'false',
        'from-asid': 'test',
        'Content-Type': 'application/json',
        'ods-code': 'test'
    }

    for url in urls:
        print('Checking: ' + url)
        try:
            response = http.request(
                'POST',
                url,
                body=json.dumps('test'),
                headers=headers,
                timeout=15.0
            )
            print('{status_code}'.format(status_code=response.status))
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    args = _parse_arguments()

    main(args.target_group_arns)

    _check_services_healthchecks()

    _send_outbound_post()