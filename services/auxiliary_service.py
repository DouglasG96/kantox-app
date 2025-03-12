import os
import boto3
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the default boto3 session using environment variables
aws_region = os.getenv('AWS_REGION', 'us-east-1')

# Initialize boto3 session without a profile
boto3.setup_default_session(region_name=aws_region)

# Initialize Flask app
app = Flask(__name__)

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

# Initialize Auxiliary Service
aux_service = AuxiliaryService()

@app.route('/s3/buckets', methods=['GET'])
def list_s3_buckets():
    buckets = aux_service.list_buckets()
    return jsonify({
        'buckets': buckets
    })

@app.route('/parameter-store/parameters', methods=['GET'])
def list_parameters():
    parameters = aux_service.list_parameters()
    return jsonify({
        'parameters': parameters
    })

@app.route('/parameter-store/parameter/<string:parameter_name>', methods=['GET'])
def get_parameter(parameter_name):
    value = aux_service.get_parameter(parameter_name)
    if value is not None:
        return jsonify({
            'parameter_name': parameter_name,
            'value': value
        })
    else:
        return jsonify({
            'message': 'Parameter not found'
        }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)