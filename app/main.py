"""
poetry run uvicorn app.main:fastapi_app
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core import load_config


settings = load_config()

fastapi_app = FastAPI()
