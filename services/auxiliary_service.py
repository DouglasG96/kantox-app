# auxiliary_service.py
import os
import boto3
from dotenv import load_dotenv  # Import python-dotenv

# Load environment variables from .env file
load_dotenv()


# Set up the default boto3 session using environment variables
aws_profile = os.getenv('AWS_PROFILE', 'default')  # Fall back to 'default' if not set
aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Fall back to 'us-east-1' if not set

boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
class AuxiliaryService:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.ssm_client = boto3.client('ssm')
    
    def list_buckets(self):
        response = self.s3_client.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]

    def list_parameters(self):
        response = self.ssm_client.describe_parameters()
        return [param['Name'] for param in response.get('Parameters', [])]
    
    def get_parameter(self, parameter_name):
        response = self.ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value'] if 'Parameter' in response else None