from fastapi import FastAPI
from app.routers import api, health
from app.middleware.metrics_middleware import MetricsMiddleware
from prometheus_client import make_asgi_app

app = FastAPI()

# Middleware for metrics
app.add_middleware(MetricsMiddleware)

# Routers
app.include_router(api.router)
app.include_router(health.router)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

