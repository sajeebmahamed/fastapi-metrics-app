# Metrics Monitoring System
## A comprehensive application that implements both system-level and application-level metrics monitoring using Prometheus metrics format. The application exposes detailed performance metrics for monitoring infrastructure health and application behavior.

## Features
### System Metrics
- **CPU Monitoring**: Process CPU time, system CPU usage percentage
- **Memory Monitoring**: Physical memory (RSS), virtual memory (VMS), system memory usage
- **Process Monitoring**: File descriptors, thread count, process uptime
- **Disk Monitoring**: Disk usage percentage by mount point
- **Application Info**: Process details, Python version, command line arguments
### HTTP Request Metrics
- **Request Volume**: Total HTTP requests with method, endpoint, and status code labels
- **Request Performance**: Request duration histograms with customizable buckets
- **Request/Response Size**: Size histograms for requests and responses
- **Active Requests**: Real-time count of active HTTP requests
- **Error Tracking**: HTTP error rates and patterns

### Application Health
- **Health Checks**: Basic, detailed endpoints
- **System Monitoring**: CPU, memory, and disk usage thresholds
- **Uptime Tracking**: Application start time and uptime metrics

## Project Structure
```bash
fastapi-metrics-app/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration management
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── system_metrics.py        # CPU, memory, disk metrics
│   │   └── http_metrics.py          # HTTP request metrics
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── metrics_middleware.py    # HTTP metrics collection middleware
│   └── routers/
│       ├── __init__.py
│       ├── api.py                   # Business logic endpoints
│       └── health.py                # Health check endpoints
├── prometheus/
│   └── prometheus.yml               # Prometheus configuration
├── docker-compose.yml               # Multi-service deployment
├── Dockerfile                       # FastAPI container
├── requirements.txt                 # Python dependencies
├── start.py                        # Application startup script
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

## Technical Stack

### Core Framework
- FastAPI: Modern web framework with automatic API documentation
- Python 3.10+: Runtime environment
- Uvicorn: High-performance ASGI server
- Pydantic: Data validation and serialization

### Monitoring Stack
- Prometheus Client: Metrics collection and exposition
- Prometheus: Time-series database and monitoring system
- Grafana: Visualization and dashboard platform

### System Monitoring
- psutil: Cross-platform system and process utilities
- Custom Middleware: HTTP request/response metrics collection

## Run the Project

### Option 1: Using Docker Compose
1. Start the services:

   ```bash
   git clone <your-repo>
   cd fastapi-metrics-app
   docker-compose up --build
   ```
2. Access the services in your browser or via API clients.

   ```bash
      - FastAPI App: http://localhost:8000
      - API Documentation: http://localhost:8000/docs
      - Prometheus: http://localhost:9090
      - Grafana: http://localhost:3000
      - Metrics: http://localhost:8000/metrics
   ```


### Option 2: Using Local Environment
1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   python start.py
   # or
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Core
- **GET** `/`: Root endpoint with application info
- **GET** `/docs`: Swagger UI for API documentation.
- **GET** `/metrics`:  Interactive API documentation.

### Data
- **GET** `/data`: Retrieve all data.
- **POST** `/data`: Create new data entry.

### Health Check
- **GET** `/health`: Basic health check.
- **GET** `/health`: Detailed health with system info.



## Metrics Reference

| Metric Name       | Type       | Description                       | Labels                       |
|---------------|------------|-----------------------------------|------------------------------|
| process_cpu_seconds_total   | Gauge      | Total CPU time consumed       | -                |
| process_resident_memory_bytes | Gauge    | process_resident_memory_bytes              | - |
| process_virtual_memory_bytes | Gauge    | Virtual memory allocated     | -                |
| process_start_time_seconds   | Gauge      | Process start time            | -                |
| process_open_fds             | Gauge      | Open file descriptors         | -                |
| process_threads              | Gauge      | Number of threads             | -                |
| system_cpu_usage_percent     | Gauge      | System CPU usage percentage   | -                |
| system_memory_usage_percent  | Gauge      | System memory usage percentage| -                |
| system_disk_usage_percent    | Gauge      | Disk usage percentage         | mountpoint                  |


## HTTP Metrics
| Metric Name                | Type       | Description                       | Labels                       |
|----------------------------|------------|-----------------------------------|------------------------------|
| http_requests_total        | Counter    | Total HTTP requests               | method, endpoint, status_code |
| http_request_duration_seconds | Histogram | Request duration                  | method, endpoint            |
| http_request_size_bytes    | Histogram  | Request size                      | method, endpoint            |
| http_response_size_bytes   | Histogram  | Response size                     | method, endpoint, status_code |
| http_requests_active       | Gauge      | Active HTTP requests              | method, endpoint |
| http_last_request_time_seconds | Gauge  | Last request timestamp            | -                            | 
| application_start_time_seconds | Gauge | Application start time            | -                            |

## Example Prometheus Queries

```bash
   # Request rate (requests per second)
   rate(http_requests_total[5m])

   # 95th percentile latency
   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

   # Error rate
   rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m])

   # CPU usage rate
   rate(process_cpu_seconds_total[5m])

   # Memory usage trend
   process_resident_memory_bytes
```

> Grafana Login → **admin / admin** (default)
