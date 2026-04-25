import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.aws_service import (
    delete_object,
    generate_download_url,
    list_objects,
    send_sns_notification,
    upload_file_to_s3,
)
from services.settings import get_settings

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "templates"))
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _render_home(request: Request, context: dict | None = None):
    base_context = {"objects": []}
    try:
        base_context["objects"] = list_objects()
    except Exception as exc:
        base_context["error"] = str(exc)
    if context:
        base_context.update(context)
    return templates.TemplateResponse(request=request, name="index.html", context=base_context)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return _render_home(request)

@router.post("/", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    try:
        settings = get_settings()
        if not file.filename:
            raise ValueError("A filename is required.")

        extension = Path(file.filename).suffix.lower()
        if extension not in settings.allowed_extensions:
            raise ValueError(f"Unsupported file extension: {extension}")

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        max_bytes = settings.max_upload_mb * 1024 * 1024
        if file_size > max_bytes:
            raise ValueError(
                f"File too large. Maximum allowed size is {settings.max_upload_mb} MB."
            )

        object_key = f"{settings.object_prefix}{uuid4().hex}{extension}"
        file_url = upload_file_to_s3(file.file, object_key)
        send_sns_notification(file.filename, file_url)

        return _render_home(
            request,
            context={
                "message": "File uploaded successfully!",
                "file_url": file_url,
                "original_name": file.filename,
            },
        )

    except Exception as e:
        return _render_home(request, context={"error": str(e)})


@router.get("/download/{object_key:path}")
async def download(object_key: str):
    url = generate_download_url(object_key)
    return RedirectResponse(url=url, status_code=307)


@router.post("/delete", response_class=HTMLResponse)
async def remove_object(request: Request, object_key: str = Form(...)):
    try:
        delete_object(object_key)
        return _render_home(request, context={"message": "File deleted successfully!"})
    except Exception as e:
        return _render_home(request, context={"error": str(e)})