"""Logging middleware for request/response tracking"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("app.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started 1",
            extra={
                "client_addr": request.client.host,
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
                "client_addr": request.client.host,
                "request_line": f"{request.method} {request.url.path}",
                "status_code": response.status_code,
                "process_time": f"{process_time:.2f}s"
            }
        )
        
        return response