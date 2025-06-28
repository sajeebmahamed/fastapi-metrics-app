# Metrics Monitoring System

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
├── prometheus
│   └── prometheus.yml          # Prometheus scrape config
├── Dockerfile                  # FastAPI image build setup
├── docker-compose.yml          # Runs app + Prometheus + Grafana
├── requirements.txt            # Project dependencies
└── README.md                   # Project overview
```

## Run the Project

### Using Docker Compose
1. Start the services:
   ```bash
   docker-compose up --build
   ```

### Using Local Environment
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Access Services

| Service       | URL                       |
|---------------|----------------------------|
| FastAPI App   | http://localhost:8000     |
| Metrics       | http://localhost:8000/metrics |
| Prometheus    | http://localhost:9090     |
| Grafana       | http://localhost:3000     |

> Grafana Login → **admin / admin** (default)
