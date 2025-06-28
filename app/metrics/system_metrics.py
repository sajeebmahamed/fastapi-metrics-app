import psutil
import threading
import time 
from prometheus_client import Gauge

cpu_usage = Gauge("process_cpu_seconds_total", "Total CPU time consumed")
memory_rss = Gauge("process_resident_memory_bytes", "Physical memory used")
memory_vms = Gauge("process_virtual_memory_bytes", "Virtual memory allocated")

def collect_system_metrics():
    while True:
        cpu_usage.set(psutil.cpu_times().user)
        memory_info = psutil.virtual_memory()
        memory_rss.set(memory_info.used)
        memory_vms.set(memory_info.total)
        time.sleep(5)  # configurable interval


# Run this in background during app startup
threading.Thread(target=collect_system_metrics, daemon=True).start()