from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.aws_service import upload_file_to_s3, send_sns_notification

import os
router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    try:
        file_url = upload_file_to_s3(file.file, file.filename)
        send_sns_notification(file.filename, file_url)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": "File uploaded successfully!", "file_url": file_url}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e)}
        )