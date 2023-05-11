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

ORIGINS = os.getenv("ORIGINS")

environment = os.getenv("ENVIRONMENT")
print(os.getcwd(), environment)
if environment == 'PROD':

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins= ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
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
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(api_v1_router, prefix='/api/v1')

@app.get("/")
async def root():
    """
    Index Page
    """
    return {
        "message": "Hello World!"
    }
