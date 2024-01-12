from fastapi import FastAPI

from app.api import analysis_controller

app = FastAPI()

app.include_router(analysis_controller.router, tags=["Analysis"])
