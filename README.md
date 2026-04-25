# EC2 S3 SNS FastAPI Project

## Description
This is a FastAPI web application that allows users to upload files to an AWS S3 bucket. After a successful upload, the app sends a notification to an AWS SNS topic. The app demonstrates integration with AWS S3 for file storage and AWS SNS for notifications.

## Features
- Upload files via a web form
- Store files in an S3 bucket (public-read)
- Send SNS notification with file details after upload

## Project Structure
```
ec2-s3-project/
├── main.py
├── controllers/
│   └── upload_controller.py
├── services/
│   └── aws_service.py
├── templates/
│   └── index.html
```

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- boto3
- AWS credentials with S3 and SNS permissions

## Setup & Run
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # then edit .env with your real values
   ```
   The app auto-loads variables from `.env`.
4. **Configure AWS credentials** (via environment variables, AWS CLI, or `~/.aws/credentials`)
5. **Run the app**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
6. **Health check**:
   - `GET /health` should return `{"status":"ok"}`
7. **Open your browser** at [http://127.0.0.1:8080](http://127.0.0.1:8080)

## Run Tests
```bash
pytest -q
```

## Production Notes
- Bucket name and topic ARN are loaded from environment variables (no hardcoded secrets).
- Upload file type and size are validated before upload.
- Uploaded object names are randomized under the `uploads/` prefix.
- Uploaded objects are listed on the home page with download and delete actions.
- Downloads use a pre-signed URL controlled by `DOWNLOAD_EXPIRY_SECONDS`.
- Set `S3_MAKE_PUBLIC=true` only when public object access is intentionally required.
# Pythons3snsec2-projec
