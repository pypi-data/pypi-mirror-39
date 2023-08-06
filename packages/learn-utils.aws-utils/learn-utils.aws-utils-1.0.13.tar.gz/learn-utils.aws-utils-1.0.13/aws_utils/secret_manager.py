# coding=utf-8
"""
module secret_manager.py
-------------------------
    | A Secret Manager Client implementation.
    | Provides classes and functions to interact with the AWS Secrets Manager service.
"""
import boto3
import os
from io import BytesIO
import botocore
import base64
from botocore.exceptions import ClientError

class SecretManagerCli(object):
    """
    A simple Secret manager client.
    """

    def __init__(self, endpoint_url=None, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        """
        SecretManager initializer.
        :param endpoint_url: s3 endpoint url to be used.
        *DEFAULT*=None
        If default value boto3 will resolve the url endpoint and send all requests to the aws.

        :param aws_access_key_id: The aws acess key to be used by the client.
        *Default*=None
        If None is passed then boto will try to find t automatically on the aws configurations.
        For more information on that please look at the boto3 docs.

        :param aws_secret_access_key: The aws secret access key to be used by the client.
        *Default*=None
        If None is passed then boto will try to find t automatically on the aws configurations.
        For more information on that please look at the boto3 docs.

        :param region_name: aws region. *e.g. 'us-east-1'
        """
        self.secret_manager = boto3.resource(
            'secretsmanager',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_secret(self, secret_name):
        """
        Gets the secre value by its name.
        :param secret_name: the secret name.
        :return: the decrypted secret.
        """
        response = self.secret_manager.get_secret_value(
            SecretId=secret_name
        )
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in response:
            secret = response['SecretString']
        else:
            secret = base64.b64decode(response['SecretBinary'])
        return secret

        # except ClientError as e:
        #     if e.response['Error']['Code'] == 'DecryptionFailureException':
        #         # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
        #         # Deal with the exception here, and/or rethrow at your discretion.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InternalServiceErrorException':
        #         # An error occurred on the server side.
        #         # Deal with the exception here, and/or rethrow at your discretion.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InvalidParameterException':
        #         # You provided an invalid value for a parameter.
        #         # Deal with the exception here, and/or rethrow at your discretion.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InvalidRequestException':
        #         # You provided a parameter value that is not valid for the current state of the resource.
        #         # Deal with the exception here, and/or rethrow at your discretion.
        #         raise e
        #     elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        #         # We can't find the resource that you asked for.
        #         # Deal with the exception here, and/or rethrow at your discretion.
        #         raise e