"""Logging middleware for request/response tracking"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("app.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Process request and log details"""
        start_time = time.time()
        
        # Get client info safely
        client_host = "unknown"
        if request.client and hasattr(request.client, "host"):
            client_host = request.client.host
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "client_addr": client_host,
                "request_line": f"{request.method} {request.url.path}",
                "status_code": "PENDING"
            }
        )
        
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "client_addr": client_host,
                "request_line": f"{request.method} {request.url.path}",
                "status_code": response.status_code,
                "process_time": f"{process_time:.2f}s"
            }
        )
        
        return response