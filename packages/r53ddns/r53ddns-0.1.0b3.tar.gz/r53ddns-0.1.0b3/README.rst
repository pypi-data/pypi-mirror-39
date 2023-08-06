r53ddns
=======

r53ddns (Route 53 Dynamic DNS) is a simple command-line utility used to update
an AWS Route 53 DNS entry with the current public IP Address of the executing
host. Used to maintain DNS records which point to a dynamic address.

r53ddns utilizes the boto3 Python API to interface with AWS.

Usage
-----

From the commandline or via systemd/cron service.
A valid AWS credential file is required for the user executing the utility. This
is typically placed in ~/.aws/credentials or the credentials may be specified
using environment variables.

.. code-block::

    [default]
    aws_access_key_id = ACCESSKEY-ID
    aws_secret_access_key = SECRET-KEY
    region = us-west-2

The user associated with the access key requires the following AWS permissions:

- route53:ChangeResourceRecordSets
- route53:ListResourceRecordSets

Optionally the following permission is required to permit SNS notifications
(used with the --notify option or environment variable):

- sns:Publish


An example AWS JSON Policy document might look like:

.. code-block::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "1",
                "Effect": "Allow",
                "Action": "sns:Publish",
                "Resource": "arn:aws:sns:REGION:ACCT-NO:TOPIC-NAME"
            },
            {
                "Sid": "2",
                "Effect": "Allow",
                "Action": [
                    "route53:ChangeResourceRecordSets",
                    "route53:ListResourceRecordSets"
                ],
                "Resource": "arn:aws:route53:::hostedzone/ZONEID"
            }
        ]
    }

*Note the Resource qualifiers should be replaced with valid Resource ARN's if utilized.*

Installation
------------

Requirements:

- Python >= 3.6.x

Using venv & pip
^^^^^^^^^^^^^^^^

.. code-block::

    python3 -m venv venv
    source venv/bin/activate
    pip install dnsupdater

Installation as a daemon using Systemd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create/install systemd service and timer unit files.
.timer will execute the .service file periodically upon boot of the OS, and
every 5 minutes thereafter.

.. code-block::

    [Unit]
    Description=route53 dynamic dns update client
    After=network.target

    [Service]
    Type=oneshot
    User=awsuser
    Environment="PATH=/opt/r53ddns/venv/bin"
    ExecStart=/opt/r53ddns/venv/bin/dnsupdater

    [Install]
    WantedBy=network.target


.. code-block::

    [Unit]
    Description=Execute r53ddns periodically

    [Timer]
    OnBootSec=1min
    OnUnitActiveSec=5min

    [Install]
    WantedBy=timers.target
