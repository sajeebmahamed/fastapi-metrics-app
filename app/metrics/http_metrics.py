from prometheus_client import Counter, Histogram, Gauge
from app.metrics.system_metrics import METRICS_REGISTRY
import time

# HTTP Request Metrics using our custom registry
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
    registry=METRICS_REGISTRY
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float('inf')],
    registry=METRICS_REGISTRY
)

REQUEST_SIZE = Histogram(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "endpoint"],
    buckets=[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, float('inf')],
    registry=METRICS_REGISTRY
)

RESPONSE_SIZE = Histogram(
    "http_response_size_bytes",
    "HTTP response size in bytes",
    ["method", "endpoint", "status_code"],
    buckets=[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, float('inf')],
    registry=METRICS_REGISTRY
)

# Active requests gauge
ACTIVE_REQUESTS = Gauge(
    "http_requests_active",
    "Number of active HTTP requests",
    ["method", "endpoint"],
    registry=METRICS_REGISTRY
)

# Request rate gauge (requests per second)
REQUEST_RATE = Gauge(
    "http_requests_per_second",
    "HTTP requests per second",
    ["method", "endpoint"],
    registry=METRICS_REGISTRY
)

# Error rate gauge
ERROR_RATE = Gauge(
    "http_errors_per_second",
    "HTTP errors per second",
    ["method", "endpoint"],
    registry=METRICS_REGISTRY
)

# Metrics for tracking application health
LAST_REQUEST_TIME = Gauge(
    "http_last_request_time_seconds",
    "Timestamp of the last HTTP request",
    registry=METRICS_REGISTRY
)

# Application uptime
APPLICATION_START_TIME = Gauge(
    "application_start_time_seconds",
    "Application start time in seconds since epoch",
    registry=METRICS_REGISTRY
)

# Initialize application start time
APPLICATION_START_TIME.set(time.time())

def record_request_metrics(method: str, endpoint: str, status_code: int, duration: float, request_size: int = 0, response_size: int = 0):
    """
    Record metrics for an HTTP request
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: Request endpoint/path
        status_code: HTTP status code
        duration: Request duration in seconds
        request_size: Size of request in bytes
        response_size: Size of response in bytes
    """
    # Record request count
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    
    # Record request latency
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)
    
    # Record request size if provided
    if request_size > 0:
        REQUEST_SIZE.labels(
            method=method,
            endpoint=endpoint
        ).observe(request_size)
    
    # Record response size if provided
    if response_size > 0:
        RESPONSE_SIZE.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).observe(response_size)
    
    # Update last request time
    LAST_REQUEST_TIME.set(time.time())

def increment_active_requests(method: str, endpoint: str):
    """Increment active requests counter"""
    ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()

def decrement_active_requests(method: str, endpoint: str):
    """Decrement active requests counter"""
    ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()

def get_application_uptime():
    """Get application uptime in seconds"""
    return time.time() - APPLICATION_START_TIME._value._value