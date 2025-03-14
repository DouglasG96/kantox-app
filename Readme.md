# 🚀 Main API

This project deploys the auxiliary API for retrieving values from AWS services using specific endpoints.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed and configured:

### 1. **Python Version 3** 🛠️  
Install Python from the [official website](https://www.python.org/downloads/).

---

## 🛠️ Setup Instructions and Run

### 1. Install pip
Ensure you have `pip` installed:
```bash
python -m ensurepip --default-pip
```

### 2. Install Dependencies
Install the required Python dependencies:
```bash
pip install Flask==2.3.2 boto3==1.28.32 python-dotenv==1.0.0 requests==2.31.0
```

### 🔑 3. Create a .env File  
Create a `.env` file with the following structure and values:
```bash
AWS_REGION="<your_region>"
MAIN_API_VERSION="<your_version>"
AUXILIARY_SERVICE_URL="<http://auxiliary_api_host>"
PORT="<your_port>"
```

### 4. Run the API
Execute the following command to start the API:
```bash
python main_api.py
```

## 📡 API Testing Guide

To test API deployments, use the following examples:

### 1. Check S3 Buckets:
```bash
curl -X GET http://localhost:6000/
```

Expected response:
```json
{
    auxiliary_version: "<your_auxiliary_api_version>",
    buckets: [
        "<your_bucket_1>",
        "<your_bucket_2>"
    ],
    version: "<your_main_api_version>"
}
```

### 2. Get all Parameters from parameter store:
```bash
curl -X GET http://localhost:6000/api/parameter-store/parameters
```
Expected response:
```json
{
    auxiliary_version: "<your_auxiliary_api_version>",
    parameters: [
        "<your_parameter_1>",
        "<your_parameter_2>"
    ],
    version: "<your_main_api_version>"
}
```

### 3. Get specific parameter from parameter store:
```bash
curl -X GET http://localhost:6000/api/parameter-store/parameter/<parameter_name>
```
Expected response:
```json
{
  "auxiliary_version": "your_auxiliary_api_version",
  "parameter_name": "your_parmeter_name",
  "value": "your_parameter_value",
  "version": "<your_main_api_version>"
}
```

---


## 🙏 Acknowledgments

- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [dotenv Documentation](https://pypi.org/project/python-dotenv/)

Happy hacking! 🎉