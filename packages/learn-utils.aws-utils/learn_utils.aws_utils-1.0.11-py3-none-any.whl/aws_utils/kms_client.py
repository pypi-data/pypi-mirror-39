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

class KMSCli(object):
    """
    A simple KMS client.
    """

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name="sa-east-1"):
        """
        KMS initializer.

        :param aws_access_key_id: The aws acess key to be used by the client.
        *Default*=None
        If None is passed then boto will try to find t automatically on the aws configurations.
        For more information on that please look at the boto3 docs.

        :param aws_secret_access_key: The aws secret access key to be used by the client.
        *Default*=None
        If None is passed then boto will try to find t automatically on the aws configurations.
        For more information on that please look at the boto3 docs.

        """
        self.kms = boto3.client(
            'kms',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def decrypt(self, encrypted_data):
        """
        Gets the secre value by its name.
        :param encrypted_data: the secret name.
        :return: the decrypted secret.
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()

        response = self.kms.decrypt(
            CiphertextBlob=base64.b64decode(encrypted_data)
        )

        if "Plaintext" in response:
            return response['Plaintext'].decode()
        return None

    def encrypt(self, key_id, plainText):
        """
        Gets the secre value by its name.
        :param key_id: secret id
        :param plainText: secret plain text.
        :return: the decrypted secret.
        """
        response = self.kms.encrypt(
            KeyId=key_id,
            Plaintext=plainText
        )
        if "CiphertextBlob" in response:
            blob = response['CiphertextBlob']
            return base64.b64encode(blob)

        return None
