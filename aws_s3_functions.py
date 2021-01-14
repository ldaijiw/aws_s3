import logging
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region="eu-west-1"):
    '''
    Create S3 bucket in specified region, defaults to eu-west-1
    '''

    # create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)

        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f"{bucket['Name']}")


def upload_file(file_name, bucket, object_name=None):
    '''
    Upload file to S3 bucket
    
    object_name: S3 object name, if none specified then defaults to file_name
    '''

    if object_name is None:
        object_name = file_name

    # upload file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

