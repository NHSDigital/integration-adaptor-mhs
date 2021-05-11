"""A script that checks that AWS load balancers have all healthy targets. For use in CI builds."""

import argparse
import sys
import requests
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

    base_url = 'https://mhs-{service}.build.nhsredteam.internal.nhs.uk/healthcheck'

    for service in ['outbound', 'inbound', 'route']:
        url = base_url.format(service=service)
        response = requests.get(url, verify=False, timeout=5)
        print('{service}: {status_code}'.format(service=service, status_code=str(response.status_code)))


if __name__ == '__main__':
    args = _parse_arguments()

    main(args.target_group_arns)

    _check_services_healthchecks()