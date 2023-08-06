# -*- coding: utf-8 -*-
import os
import sys
import logging
import argparse
import urllib.request

import boto3

from . import __version__, __description__

log = logging.getLogger(__name__)
LOG_NOTIFY = 60
ENV_RECORD = "RECORD"
ENV_ZONEID = "ZONEID"
ENV_NOTIFY = "NOTIFY"


def parse_args(argv=None):
    args = argv or sys.argv[1:]

    parser = argparse.ArgumentParser(prog=sys.argv[0], allow_abbrev=True,
                                     description=__description__)
    parser.add_argument('--version', action='version', version=__version__,
                        help='Display version information.')
    parser.add_argument('--record', action='store',
                        help=f'Supply the fully qualified domain record name. '
                             f'This can also be provided by the environment '
                             f'variable "{ENV_RECORD}"')
    parser.add_argument('--zoneid', action='store',
                        help=f'Supply the Route 53 Domain ZONE ID. This can '
                             f'also be provided using the environment variable '
                             f'"{ENV_ZONEID}"')
    parser.add_argument('--create', action='store_true',
                        help='If the record does not exist, it will be '
                             'created. If --create is not specified and the '
                             'record does not exist, execution will fail.')
    parser.add_argument('--notify', action='store', dest='topic_arn',
                        help=f'Optionally provide an SNS Topic ARN where a '
                             f'notification will be published on record change.'
                             f' This can also be provided using the environment'
                             f' variable "{ENV_NOTIFY}"')
    parser.add_argument('--dryrun', action='store_true',
                        help='Do a dry-run where current IP and record values '
                             'will be displayed, but no changes will be made.')
    parser.add_argument('--verbosity', '-v', action='count', default=0,
                        help='Increase log message verbosity.')

    return parser.parse_args(args)


def get_public_ip():
    return urllib.request.urlopen('https://api.ipify.org').read().decode('utf-8')


def get_current_record_value(client, zoneid, record_name, record_type='A'):
    """Retrieves the current value of the specified record from AWS Route 53

    The record_name must match exactly the name of an existing record,
    else None will be returned. The DNS root domain (a trailing '.') is
    automatically appended to the record_name for comparison if it isn't
    supplied.

    Parameters
    ----------
    client
    zoneid
    record_name
    record_type

    Returns
    -------
    str or None
    If the record exists and exactly matches record_name, the current value
    is returned, else the value None is returned.

    """
    if record_name[-1] != '.':
        record_name = record_name + '.'

    resp = client.list_resource_record_sets(
        HostedZoneId=zoneid,
        StartRecordName=record_name,
        StartRecordType=record_type,
        MaxItems='1'
    )
    record_sets = resp['ResourceRecordSets'][0]
    if record_sets.get('Name', None) == record_name:
        return record_sets['ResourceRecords']
    else:
        return None


def upsert_record(client, zoneid, record_name, value, record_type='A', ttl=300):
    """Updates or Creates the specified AWS Route 53 domain resource record

    Parameters
    ----------
    client: boto3.client
        The boto3 'route53' client to utilize for the update request
    zoneid: str
        The Route 53 Hosted Zone ID where the record to be created/updated
        resides
    record_name: str
        The fully qualified name for the DNS record to be created/updated. Note:
        the trailing top-level '.' is optional in this context.
    value: str
        The value which the record will be updated to. Typically the IP address.
    record_type: str
        The record type to create/update. One of:
        'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA'
    ttl: int, Optional
        Set the TTL (Time To Live) of the record in seconds. Defaults to 300s

    See Also
    --------
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets

    Returns
    -------
    dict:

        {
            'Id': 'string',
            'Status': 'PENDING'|'INSYNC',
            'SubmittedAt': datetime(year, month, day),
            'Comment': 'string'
        }

    """
    response = client.change_resource_record_sets(
        HostedZoneId=zoneid,
        ChangeBatch={
            'Comment': 'Update record initiated by r53ddns.py',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [
                            {'Value': value}
                        ]
                    }
                }
            ]
        }
    )
    return response['ChangeInfo']


def run():
    stream_hdlr = logging.StreamHandler(sys.stderr)
    stream_hdlr.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s :: '
                                               '%(message)s'))
    log.addHandler(stream_hdlr)

    opts = parse_args()
    if opts.verbosity > 1:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.ERROR)

    record = opts.record or os.getenv(ENV_RECORD, None)
    zoneid = opts.zoneid or os.getenv(ENV_ZONEID, None)

    if not all([x is not None for x in {record, zoneid}]):
        log.critical('Record Name or Zone ID not supplied. Set RECORD/ZONEID '
                     'environement variables, or supply via arguments.')
        return 1

    notify = opts.topic_arn or os.getenv(ENV_NOTIFY, None)
    if notify:
        from .sns_notify import SNSHandler
        sns_hdlr = SNSHandler(notify)
        sns_hdlr.setLevel(LOG_NOTIFY)
        log.addHandler(sns_hdlr)

    client = boto3.client('route53')
    record_value = get_current_record_value(client, zoneid, record)
    if not record_value and not opts.create:
        log.critical(f'Record {record} does not exist and --create not '
                     f'specified, aborting.')
        return 1
    elif not record_value and opts.create:
        log.info(f'Record {record} does not exist and will be created.')

    new_value = get_public_ip()
    if record_value == new_value:
        log.info('Route 53 record already matches public IP address')
        return 0

    # Update Route 53 Record to new Public IP value
    if opts.dryrun:
        log.info(f'DryRun: Record {record} in zone {zoneid}, would be updated '
                 f'to value: {new_value}, from current value: {record_value}.')
        return 0

    change_info = upsert_record(client, zoneid, record,
                                value=new_value, record_type='A')
    message = f'DNS Record {record} in zone {zoneid}, value updated to ' \
              f'{new_value}, with status: {change_info["Status"]},'\
              f' at {change_info["SubmittedAt"]}'
    log.log(LOG_NOTIFY, message)
    log.info(message)
    return 0
