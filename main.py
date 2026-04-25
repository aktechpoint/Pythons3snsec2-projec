from fastapi import FastAPI
from controllers.upload_controller import router

app = FastAPI(
    title="EC2 S3 SNS Uploader",
    version="1.0.0",
    description="Upload files to S3 and notify via SNS.",
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}