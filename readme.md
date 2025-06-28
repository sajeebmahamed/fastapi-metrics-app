# FastAPI Metrics Monitoring System Documentation

## Features
- **CPU & Memory Monitoring** using `psutil`
- **HTTP Request Metrics** using custom middleware
- **Prometheus-Compatible Metrics** via `/metrics` endpoint

## Project Structure
```bash
.
├── app
│   ├── main.py                  # FastAPI app with middleware and routing
│   ├── config.py                # Placeholder for configs
│   ├── metrics
│   │   ├── system_metrics.py    # CPU & memory monitoring
│   │   └── http_metrics.py      # HTTP request counters & histograms
│   ├── middleware
│   │   └── metrics_middleware.py # Records request time & status
│   └── routers
│       ├── api.py               # Sample /data endpoints
│       └── health.py            # /health check endpoint
├── requirements.txt            # Project dependencies
└── README.md                   # Project overview
```

## Run the Project
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
2. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```
3. Access the app at `http://localhost:8000`.
4. View metrics at `http://localhost:8000/metrics`.
## Endpoints
- **GET /data**: Returns a sample data response.
- **GET /health**: Returns a health check response.
- **GET /metrics**: Provides Prometheus-compatible metrics.
