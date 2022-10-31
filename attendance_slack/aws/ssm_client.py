import logging
import traceback

import boto3
from boto3.session import Session


class AwsSsmClient:
    def __init__(self, profile: str = None):
        if profile is None:
            self.ssm = boto3.client("ssm")
        else:
            session = Session(profile_name=profile)
            self.ssm = session.client("ssm")

    def get_parameter(self, name: str) -> str:
        try:
            logging.info("start: get patameter.")
            response = self.ssm.get_parameter(Name=name, WithDecryption=True)
            logging.info("finish: get parameter.")
            return response["Parameter"]["Value"]
        except Exception as e:
            logging.error(
                f"return NG response from AWS. reason: {traceback.format_exc()}"
            )
            raise e

    def put_parameter(
        self,
        name: str,
        value: str,
        key_id: str,
        type: str = "SecureString",
        override: bool = True,
    ) -> None:
        try:
            logging.info("start: put patameter.")
            self.ssm.put_parameter(
                Name=name,
                Value=value,
                Type=type,
                KeyId=key_id,
                Overwrite=override,
            )
            logging.info("finish: put patameter.")
        except Exception as e:
            logging.error(
                f"return NG response from AWS. reason: {traceback.format_exc()}"
            )
            raise e
