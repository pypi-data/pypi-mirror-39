# -*- coding: utf-8 -*-
import logging
import boto3


class SNSHandler(logging.Handler):
    """Simple SNS Logging Handler

    All log records received above the logging level will be sent
    to the SNS topic ARN provided during initialization.

    """
    def __init__(self, topic_arn, subject=None):
        super().__init__()
        self.client = boto3.client('sns')
        self.subject = subject or 'DNS Updater Notification'
        self.arn = topic_arn

    def emit(self, record):
        message = self.format(record)

        self.client.publish(
            TopicArn=self.arn,
            Subject=self.subject,
            Message=message
        )
