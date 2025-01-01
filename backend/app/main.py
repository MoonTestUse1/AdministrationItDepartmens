"""Main application module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, employees, requests, admin

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(employees.router, prefix="/api", tags=["employees"])
app.include_router(requests.router, prefix="/api", tags=["requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])