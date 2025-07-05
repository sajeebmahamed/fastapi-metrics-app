from fastapi import FastAPI
from app.routers import api, health
from app.middleware.metrics_middleware import MetricsMiddleware
from prometheus_client import make_asgi_app
from app.metrics.system_metrics import get_metrics_registry
import uvicorn

app = FastAPI(
    title="Metrics Monitoring System",
    description="A comprehensives application with built-in metrics collection",
    version="1.0.0"
)

# Middleware for metrics
app.add_middleware(MetricsMiddleware)

# Routers
app.include_router(api.router)
app.include_router(health.router)

# Mount Prometheus metrics endpoint with our custom registry
metrics_app = make_asgi_app(registry=get_metrics_registry())
app.mount("/metrics", metrics_app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI Metrics Monitoring System", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)