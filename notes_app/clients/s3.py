import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

aws_access_key_id = os.environ.get("aws_access_key_id")
aws_secret_access_key = os.environ.get("aws_secret_access_key")
region = 'us-east-1'
bucket = 'naprofileimgs'


class S3Uploader:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )

    def upload_file(self, file_name, object_name=None):

        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            self.client.upload_file(file_name, bucket, object_name, ExtraArgs={"ACL": "public-read"})
            logging.info(f"Successfully uploaded {file_name} to {bucket}")
            return f"Successfully uploaded {file_name} to {bucket}"
        except ClientError as e:
            logging.error(e)
            return False

    def upload_fileobj(self, file_obj, object_name):
        try:
            self.client.upload_fileobj(file_obj, bucket, object_name, ExtraArgs={"ACL": "public-read"})
            logging.info(f"Successfully uploaded {object_name} to {bucket}")
            return f"Successfully uploaded {object_name} to {bucket}"
        except ClientError as e:
            logging.error(e)
            return False


# check = S3Uploader()
# check.upload_file('/Users/carlossanchez/Desktop/test1.jpg', 'carlos_is_testing')
