# main_api.py

import sys
import os
from flask import Flask, jsonify
from dotenv import load_dotenv  # Import python-dotenv

# Load environment variables from .env file
load_dotenv()

# Versioning
MAIN_API_VERSION = os.getenv('MAIN_API_VERSION', '1.0.0')
AUXILIARY_SERVICE_VERSION = os.getenv('AUXILIARY_SERVICE_VERSION', '1.0.0')

api_dir = os.path.dirname(__file__)
service_dir = os.path.join(api_dir,'..','services')
sys.path.append(service_dir)
from auxiliary_service import AuxiliaryService 

app = Flask(__name__)


# Initialize Auxiliary Service
aux_service = AuxiliaryService()

@app.route('/api/s3/buckets', methods=['GET'])
def list_s3_buckets():
    buckets = aux_service.list_buckets()
    return jsonify({
        'version': MAIN_API_VERSION,
        'auxiliary_version': AUXILIARY_SERVICE_VERSION,
        'buckets': buckets
    })

@app.route('/api/parameter-store/parameters', methods=['GET'])
def list_parameters():
    parameters = aux_service.list_parameters()
    return jsonify({
        'version': MAIN_API_VERSION,
        'auxiliary_version': AUXILIARY_SERVICE_VERSION,
        'parameters': parameters
    })

@app.route('/api/parameter-store/parameter/<string:parameter_name>', methods=['GET'])
def get_parameter(parameter_name):
    value = aux_service.get_parameter(parameter_name)
    if value is not None:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'parameter_name': parameter_name,
            'value': value
        })
    else:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'message': 'Parameter not found'
        }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)