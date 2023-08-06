"""
Introduction
------------
Integration objects represents a single Rockset integration.
These objects are generally created using a Rockset Client
object using methods such as::

    from rockset import Client

    # connect to Rockset
    rs = Client(api_key=...)

    # create a new integration
    aws_integration = rs.Integration.AWS.create('aws-integration')
"""
from .integration import Integration

from rockset.swagger_client.api import IntegrationsApi
from rockset.swagger_client.models import (AwsKeyIntegration, CreateIntegrationRequest)

class AWSIntegration(Integration):
    @classmethod
    def create(cls, name, aws_access_key_id, aws_secret_access_key, **kwargs):

        if aws_access_key_id is None or aws_secret_access_key is None:
            raise ValueError(
                'aws_access_key_id and aws_secret_access_key required '
                'to create an AWS integration'
            )

        if 'client' not in kwargs:
            raise ValueError(
                'incorrect API usage.'
                'use rockset.Client().Integrations.AWS.create() instead'
            )

        client = kwargs.pop('client')

        aws_credentials = AwsKeyIntegration(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)

        request = CreateIntegrationRequest(
                name=name,
                aws=aws_credentials,
                **kwargs
                )

        integration = IntegrationsApi(client).create(body=request).get('data')
        return cls(client, **integration.to_dict())

    def __init__(self, *args, **kwargs):
        kwargs['type'] = Integration.TYPE_AWS
        super().__init__(*args, **kwargs)
