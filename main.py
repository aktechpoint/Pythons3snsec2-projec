from fastapi import FastAPI
from controllers.upload_controller import router

app = FastAPI()

app.include_router(router)