import os
from typing import List, Optional

class Settings:
    """
    Application configuration settings
    """
    
    # Application settings
    APP_NAME: str = "FastAPI Metrics Monitoring System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Metrics settings
    METRICS_COLLECTION_INTERVAL: int = int(os.getenv("METRICS_COLLECTION_INTERVAL", "5"))
    METRICS_ENDPOINT: str = os.getenv("METRICS_ENDPOINT", "/metrics")
    
    # Middleware settings
    EXCLUDE_PATHS_FROM_METRICS: List[str] = [
        "/metrics",
        "/favicon.ico",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]
    
    # Prometheus settings
    PROMETHEUS_MULTIPROC_DIR: Optional[str] = os.getenv("PROMETHEUS_MULTIPROC_DIR")
    
    # Histogram bucket settings
    LATENCY_BUCKETS: List[float] = [
        0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 
        0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float('inf')
    ]
    
    SIZE_BUCKETS: List[float] = [
        1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, float('inf')
    ]
    
    # Health check settings
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
    CPU_THRESHOLD_WARNING: float = float(os.getenv("CPU_THRESHOLD_WARNING", "80.0"))
    CPU_THRESHOLD_CRITICAL: float = float(os.getenv("CPU_THRESHOLD_CRITICAL", "95.0"))
    MEMORY_THRESHOLD_WARNING: float = float(os.getenv("MEMORY_THRESHOLD_WARNING", "80.0"))
    MEMORY_THRESHOLD_CRITICAL: float = float(os.getenv("MEMORY_THRESHOLD_CRITICAL", "95.0"))
    DISK_THRESHOLD_WARNING: float = float(os.getenv("DISK_THRESHOLD_WARNING", "80.0"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    @classmethod
    def get_custom_buckets(cls, bucket_type: str) -> List[float]:
        """
        Get custom histogram buckets from environment variables
        """
        env_var = f"{bucket_type.upper()}_BUCKETS"
        buckets_str = os.getenv(env_var)
        
        if buckets_str:
            try:
                buckets = [float(x.strip()) for x in buckets_str.split(",")]
                # Ensure inf is included
                if buckets[-1] != float('inf'):
                    buckets.append(float('inf'))
                return buckets
            except ValueError:
                pass
        
        # Return default buckets
        if bucket_type.lower() == "latency":
            return cls.LATENCY_BUCKETS
        elif bucket_type.lower() == "size":
            return cls.SIZE_BUCKETS
        else:
            return cls.LATENCY_BUCKETS

# Create global settings instance
settings = Settings()

# Environment-specific configurations
def get_settings():
    """Get application settings"""
    return settings