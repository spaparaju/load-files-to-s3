import logging
import boto3
import os
import sys
from botocore.exceptions import ClientError

class S3Uploader:

    def __init__(self):
        print ('initializing S3 Uploader')
    
    def create_bucket(self, bucket_name, region=None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region is None:
                s3_client = boto3.client('s3')
                print (bucket_name)
                print ('creating S3 bucket ... : ' + bucket_name)
                s3_client.create_bucket(Bucket=bucket_name)
                print ('created S3 bucket ... : ' + bucket_name)

            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            print ('error...')
            return False
        return True

    def list_buckets(self):
        # Retrieve the list of existing buckets
        s3 = boto3.client('s3')
        response = s3.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_files_from_folder_to_s3(self, folder_name, bucket_name):
        for dirname, dirnames, filenames in os.walk(folder_name):
            # print path to all filenames.
            for filename in filenames:
                print (' uploading the file : '+ os.path.join(dirname, filename))
                try:
                    self.upload_file(os.path.join(dirname, filename), bucket_name)
                except ClientError as e:
                    logging.error(e)
                    return False
        return True

