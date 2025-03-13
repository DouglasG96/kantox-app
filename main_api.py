import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Versioning
MAIN_API_VERSION = os.getenv('MAIN_API_VERSION', '1.0.0')
AUXILIARY_SERVICE_VERSION = os.getenv('AUXILIARY_SERVICE_VERSION', '1.0.0')
PORT = os.getenv('PORT', 5000)

# Auxiliary Service URL
AUXILIARY_SERVICE_URL = os.getenv('AUXILIARY_SERVICE_URL', 'http://localhost:6000')

# Initialize Flask app
app = Flask(__name__)

@app.route('/api/s3/buckets', methods=['GET'])
def list_s3_buckets():
    response = requests.get(f"{AUXILIARY_SERVICE_URL}/s3/buckets")
    if response.status_code == 200:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'buckets': response.json().get('buckets', [])
        })
    else:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'message': 'Failed to fetch S3 buckets'
        }), 500

@app.route('/api/parameter-store/parameters', methods=['GET'])
def list_parameters():
    response = requests.get(f"{AUXILIARY_SERVICE_URL}/parameter-store/parameters")
    if response.status_code == 200:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'parameters': response.json().get('parameters', [])
        })
    else:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'message': 'Failed to fetch SSM parameters'
        }), 500

@app.route('/api/parameter-store/parameter/<string:parameter_name>', methods=['GET'])
def get_parameter(parameter_name):
    response = requests.get(f"{AUXILIARY_SERVICE_URL}/parameter-store/parameter/{parameter_name}")
    if response.status_code == 200:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'parameter_name': parameter_name,
            'value': response.json().get('value')
        })
    elif response.status_code == 404:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'message': 'Parameter not found'
        }), 404
    else:
        return jsonify({
            'version': MAIN_API_VERSION,
            'auxiliary_version': AUXILIARY_SERVICE_VERSION,
            'message': 'Failed to fetch parameter'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)