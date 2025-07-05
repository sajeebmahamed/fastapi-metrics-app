import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.metrics.http_metrics import (
    record_request_metrics,
    increment_active_requests,
    decrement_active_requests
)

class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect HTTP request metrics
    """
    
    def __init__(self, app, exclude_paths=None):
        super().__init__(app)
        # Default paths to exclude from metrics
        self.exclude_paths = exclude_paths or {'/metrics', '/favicon.ico'}
    
    async def dispatch(self, request: Request, call_next):
        # Skip metrics collection for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Extract request information
        method = request.method
        endpoint = request.url.path
        
        # Get request size
        request_size = 0
        if hasattr(request, 'headers'):
            content_length = request.headers.get('content-length')
            if content_length:
                try:
                    request_size = int(content_length)
                except ValueError:
                    pass
        
        # Increment active requests
        increment_active_requests(method, endpoint)
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Get response size
            response_size = 0
            if hasattr(response, 'headers'):
                content_length = response.headers.get('content-length')
                if content_length:
                    try:
                        response_size = int(content_length)
                    except ValueError:
                        pass
            
            # Record metrics
            record_request_metrics(
                method=method,
                endpoint=endpoint,
                status_code=response.status_code,
                duration=duration,
                request_size=request_size,
                response_size=response_size
            )
            
            return response
            
        except Exception as e:
            # Calculate duration for failed requests
            duration = time.time() - start_time
            
            # Record metrics for failed requests (500 status)
            record_request_metrics(
                method=method,
                endpoint=endpoint,
                status_code=500,
                duration=duration,
                request_size=request_size,
                response_size=0
            )
            
            # Re-raise the exception
            raise e
            
        finally:
            # Always decrement active requests
            decrement_active_requests(method, endpoint)