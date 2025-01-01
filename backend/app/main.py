"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import admin, employees, requests, auth

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])