from fastapi import APIRouter, HTTPException
import time
import psutil
import platform
from app.metrics.http_metrics import get_application_uptime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": get_application_uptime()
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check with system information
    """
    try:
        # Get system information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get application uptime
        uptime = get_application_uptime()
        
        # Determine overall health status
        status = "healthy"
        issues = []
        
        # Check CPU usage
        if cpu_percent > 80:
            status = "warning"
            issues.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        # Check memory usage
        if memory.percent > 80:
            status = "warning"
            issues.append(f"High memory usage: {memory.percent:.1f}%")
        
        # Check disk usage
        if (disk.used / disk.total) * 100 > 80:
            status = "warning"
            issues.append(f"High disk usage: {(disk.used / disk.total) * 100:.1f}%")
        
        # If there are critical issues, mark as unhealthy
        if cpu_percent > 95 or memory.percent > 95:
            status = "unhealthy"
        
        return {
            "status": status,
            "timestamp": time.time(),
            "uptime": uptime,
            "system": {
                "platform": platform.system(),
                "platform_version": platform.release(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            "issues": issues
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - indicates if the application is ready to serve requests
    """
    try:
        # Check if application has been running for at least 10 seconds
        uptime = get_application_uptime()
        if uptime < 10:
            raise HTTPException(
                status_code=503,
                detail="Application not ready - still starting up"
            )
        
        # Check if system resources are available
        memory = psutil.virtual_memory()
        if memory.percent > 95:
            raise HTTPException(
                status_code=503,
                detail="Application not ready - insufficient memory"
            )
        
        return {
            "status": "ready",
            "timestamp": time.time(),
            "uptime": uptime
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Readiness check failed: {str(e)}"
        )

@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - indicates if the application is alive and responsive
    """
    try:
        # Simple check to ensure the application is responsive
        current_time = time.time()
        
        # Check if we can access basic system information
        psutil.cpu_percent()
        
        return {
            "status": "alive",
            "timestamp": current_time,
            "uptime": get_application_uptime()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Liveness check failed: {str(e)}"
        )