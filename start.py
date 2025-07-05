#!/usr/bin/env python3
"""
FastAPI Metrics Monitoring System Startup Script
"""

import uvicorn
import logging
import sys
import os

# Set up basic logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def main():
    """Main startup function"""
    try:
        # Import config after logging is set up
        from app.config import settings
        
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"Host: {settings.HOST}, Port: {settings.PORT}")
        logger.info(f"Debug mode: {settings.DEBUG}")
        logger.info(f"Metrics endpoint: {settings.METRICS_ENDPOINT}")
        
        # Ensure metrics are initialized
        logger.info("Initializing metrics...")
        from app.metrics import start_metrics_collection
        start_metrics_collection()
        logger.info("Metrics collection started")
        
        # Start the application
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=False,  # Disable reload in Docker to avoid multiprocessing issues
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True,
            server_header=False,
            date_header=False
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()