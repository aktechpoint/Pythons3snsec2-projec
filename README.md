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
    sudo apt update
    sudo apt install python3-pip -y
    pip3 install fastapi uvicorn boto3 python-multipart jinja2
    pip install fastapi uvicorn boto3
   ```
3. **Configure AWS credentials** (via environment variables, AWS CLI, or `~/.aws/credentials`)
4. **Edit S3 bucket and SNS topic in `services/aws_service.py`** if needed.
5. **Run the app**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   nohup uvicorn main:app --host 0.0.0.0 --port 8080 &
   ```
6. **Open your browser** at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Notes
- Make sure your AWS credentials have permission to upload to the S3 bucket and publish to the SNS topic.
- The app is for demonstration and should not be used in production without proper security and validation.
# Pythons3snsec2-projec
