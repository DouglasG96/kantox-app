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


## 📦 GitHub Actions Workflow Definition

This project includes a GitHub Actions workflow to automate the build, push, and deployment of the **Main API** using ArgoCD and Kubernetes.

### 🚀 CI/CD Pipeline Overview

- **Build and Push Docker Image:**
  - Logs in to Docker Hub
  - Builds and pushes the Docker image

- **Deploy with ArgoCD:**
  - Clones the `kantox-k8s` repository
  - Updates the ConfigMap with a new version
  - Pushes the updated ConfigMap to trigger an ArgoCD deployment

### 🔧 GitHub Actions Workflow Steps

#### 1. **Build and Push Docker Image**
```yaml
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin ${{ env.DOCKER_REGISTRY }}

      - name: Build and push API Docker image
        run: |
          docker build -t ${{ env.DOCKER_REGISTRY }}/${{ env.DOCKER_REPOSITORY_API }}:latest .
          docker push ${{ env.DOCKER_REGISTRY }}/${{ env.DOCKER_REPOSITORY_API }}:latest
```

#### 2. **Deploy with ArgoCD**
```yaml
  deploywithargocd:
    runs-on: ubuntu-latest
    needs: build-and-push
    steps:
      - name: Clone kantox-k8s repository
        run: |
          git clone https://github.com/douglasg96/kantox-k8s.git
          cd kantox-k8s/main-api
          git config --global user.name "GitHub Actions"
          git config --global user.email "drg96@gmail.com"

      - name: Update ConfigMap version
        run: |
          CURRENT_VERSION=$(cat kantox-k8s/main-api/configmap.yaml | grep MAIN_API_VERSION | awk '{print $2}' | tr -d '"')
          NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."$2"."$3+1}')
          sed -i "s|MAIN_API_VERSION:.*|MAIN_API_VERSION: \"$NEW_VERSION\"|g" kantox-k8s/main-api/configmap.yaml
          echo "Updated MAIN_API_VERSION to $NEW_VERSION"

      - name: Commit and push changes
        run: |
          cd kantox-k8s/main-api
          git add configmap.yaml
          git commit -m "Update MAIN_API_VERSION to $NEW_VERSION"
          git push https://${{ secrets.GH_TOKEN }}@github.com/douglasg96/kantox-k8s.git HEAD:main
```
---

## 🙏 Acknowledgments

- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [dotenv Documentation](https://pypi.org/project/python-dotenv/)

Happy hacking! 🎉