"""
Foodindo App helps to automate lunch registration
and validation for Entri Office Lunch
"""
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api_v1.urls import router as api_v1_router

load_dotenv(".env")

environment = os.getenv("ENVIRONMENT")
print(os.getcwd(), environment)
if environment == 'PROD':

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

elif environment == 'DEV':
    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5500"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
# else:
#     app = FastAPI(title='FastAPI Redis Tutorial')

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(api_v1_router, prefix='/api/v1')
