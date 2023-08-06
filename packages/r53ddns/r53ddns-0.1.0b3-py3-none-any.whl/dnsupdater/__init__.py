# -*- coding: utf-8 -*-

__version__ = '0.1.0a1'
__description__ = """Simple AWS Route 53 DNS Updater.

This script will programatically update a Route 53 DNS record to the current
public IP (retrieved via ipify.org API) of the computer/network it is executed
on. Records will only be modified if the current value and public IP differ.

AWS Credentials must be available in ~/.aws/credentials with appropriate 
permissions to list and create/update Resource Record Sets in Route 53.

Optional notifications can be sent via AWS SNS given an SNS topic ARN and the
appropriate permission to publish on that topic.

"""
