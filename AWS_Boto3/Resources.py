import boto3

from AwsCli import KEY_AWS_KEY


class Resource:
    # A class for creating boto3 "Resource" interfaces to AWS services

    def __init__(self, region, aws_key, aws_secret):
        # Resource instance
        self.region = region
        self.key_id = aws_key
        self.secret_key = aws_secret

    def ec2_resource(self):
        # Create and return a Resource for interacting with EC2 instances
        ec2 = boto3.resource("ec2", aws_access_key_id=self.key_id,
                             aws_secret_access_key=self.secret_key,
                             region_name=self.region)
        return ec2

    def s3_resource(self):
        # Create and return a Resource for interacting with S3 instances
        s3 = boto3.resource("s3", aws_access_key_id=self.key_id,
                            aws_secret_access_key=self.secret_key,
                            region_name=self.region)
        return s3

    def cw_client(self):
        # Create and return a Client for interacting with CloudWatch
        cw = cloudwatch = boto3.client('cloudwatch', aws_access_key_id=self.key_id,
                                       aws_secret_access_key=self.secret_key,
                                       region_name=self.region)
        return cw

    def ec2_client(self):
        # Create and return a Client for interacting with EC2
        ec2 = boto3.client("ec2", aws_access_key_id=self.key_id,
                           aws_secret_access_key=self.secret_key,
                           region_name=self.region)
        return ec2

    def sns_client(self):
        # Create and return a Client for interacting with SNS
        sns = boto3.client("sns", aws_access_key_id=self.key_id,
                           aws_secret_access_key=self.secret_key,
                           region_name=self.region)
        return sns

    def rds_client(self):
        # Create and return a Client for interacting with RDS
        rds = boto3.client("rds", aws_access_key_id=self.key_id,
                           aws_secret_access_key=self.secret_key,
                           region_name=self.region)
        return rds