from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import logging
from logging.config import dictConfig
from .logging_config import logging_config

# Configure logging
dictConfig(logging_config)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Support Portal API",
    description="API for managing support requests and employees",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Custom OpenAPI documentation
@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="Support Portal API Documentation",
        swagger_favicon_url="/favicon.ico"
    )

@app.get("/api/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(
        title="Support Portal API",
        version="1.0.0",
        description="API for managing support requests and employees",
        routes=app.routes
    )

# Existing middleware and routes...