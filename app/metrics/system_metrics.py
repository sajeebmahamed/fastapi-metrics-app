import psutil
import threading
import time
import sys
import platform
from prometheus_client import Gauge, Info, CollectorRegistry

# Use a separate registry to avoid conflicts with default registry
METRICS_REGISTRY = CollectorRegistry()

# Global flag to track if metrics are initialized
_metrics_initialized = False
_metrics_lock = threading.Lock()

# Global metrics variables
process_cpu_seconds_total = None
process_resident_memory_bytes = None
process_virtual_memory_bytes = None
process_start_time_seconds = None
process_open_fds = None
process_threads = None
system_cpu_usage_percent = None
system_memory_usage_percent = None
system_disk_usage_percent = None
process_info = None

def initialize_metrics():
    """Initialize metrics only once"""
    global _metrics_initialized
    global process_cpu_seconds_total, process_resident_memory_bytes, process_virtual_memory_bytes
    global process_start_time_seconds, process_open_fds, process_threads
    global system_cpu_usage_percent, system_memory_usage_percent, system_disk_usage_percent
    global process_info
    
    with _metrics_lock:
        if _metrics_initialized:
            return
        
        try:
            # CPU Metrics
            process_cpu_seconds_total = Gauge(
                "process_cpu_seconds_total", 
                "Total CPU time consumed by the process",
                registry=METRICS_REGISTRY
            )

            # Memory Metrics
            process_resident_memory_bytes = Gauge(
                "process_resident_memory_bytes", 
                "Physical memory currently used",
                registry=METRICS_REGISTRY
            )

            process_virtual_memory_bytes = Gauge(
                "process_virtual_memory_bytes", 
                "Virtual memory allocated",
                registry=METRICS_REGISTRY
            )

            # Additional System Metrics
            process_start_time_seconds = Gauge(
                "process_start_time_seconds", 
                "Start time of the process since unix epoch",
                registry=METRICS_REGISTRY
            )

            process_open_fds = Gauge(
                "process_open_fds", 
                "Number of open file descriptors",
                registry=METRICS_REGISTRY
            )

            process_threads = Gauge(
                "process_threads", 
                "Number of OS threads in the process",
                registry=METRICS_REGISTRY
            )

            # System-wide metrics
            system_cpu_usage_percent = Gauge(
                "system_cpu_usage_percent", 
                "System CPU usage percentage",
                registry=METRICS_REGISTRY
            )

            system_memory_usage_percent = Gauge(
                "system_memory_usage_percent", 
                "System memory usage percentage",
                registry=METRICS_REGISTRY
            )

            system_disk_usage_percent = Gauge(
                "system_disk_usage_percent", 
                "System disk usage percentage", 
                ["mountpoint"],
                registry=METRICS_REGISTRY
            )

            # Process info
            process_info = Info(
                "process", 
                "Process information",
                registry=METRICS_REGISTRY
            )
            
            _metrics_initialized = True
            print("System metrics initialized successfully")
            
        except Exception as e:
            print(f"Error initializing metrics: {e}")
            raise

def collect_system_metrics():
    """Collect system and process metrics periodically"""
    if not _metrics_initialized:
        initialize_metrics()
    
    # Get current process
    current_process = psutil.Process()
    
    # Set process start time (only once)
    if process_start_time_seconds:
        process_start_time_seconds.set(current_process.create_time())
    
    # Set process info (only once)
    if process_info:
        try:
            process_info.info({
                'pid': str(current_process.pid),
                'name': current_process.name(),
                'cmdline': ' '.join(current_process.cmdline()),
                'cwd': current_process.cwd(),
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'platform': platform.system(),
                'platform_release': platform.release()
            })
        except Exception:
            # Some info might not be accessible
            pass
    
    while True:
        try:
            # Process CPU metrics
            if process_cpu_seconds_total:
                cpu_times = current_process.cpu_times()
                process_cpu_seconds_total.set(cpu_times.user + cpu_times.system)
            
            # Process memory metrics
            if process_resident_memory_bytes and process_virtual_memory_bytes:
                memory_info = current_process.memory_info()
                process_resident_memory_bytes.set(memory_info.rss)
                process_virtual_memory_bytes.set(memory_info.vms)
            
            # Process file descriptors
            if process_open_fds:
                try:
                    if platform.system() != "Windows":
                        fds = getattr(current_process, 'num_fds', None)
                        if fds is not None:
                            process_open_fds.set(fds())
                    else:
                        handles = getattr(current_process, 'num_handles', None)
                        if handles is not None:
                            process_open_fds.set(handles())
                except (AttributeError, psutil.AccessDenied, psutil.NoSuchProcess, OSError):
                    pass
            
            # Process threads
            if process_threads:
                process_threads.set(current_process.num_threads())
            
            # System-wide CPU usage
            if system_cpu_usage_percent:
                system_cpu_usage_percent.set(psutil.cpu_percent(interval=1))
            
            # System memory usage
            if system_memory_usage_percent:
                system_memory = psutil.virtual_memory()
                system_memory_usage_percent.set(system_memory.percent)
            
            # System disk usage
            if system_disk_usage_percent:
                try:
                    disk_usage = psutil.disk_usage('/')
                    system_disk_usage_percent.labels(mountpoint='/').set(
                        (disk_usage.used / disk_usage.total) * 100
                    )
                except (OSError, psutil.AccessDenied):
                    try:
                        disk_usage = psutil.disk_usage('C:\\')
                        system_disk_usage_percent.labels(mountpoint='C:').set(
                            (disk_usage.used / disk_usage.total) * 100
                        )
                    except (OSError, psutil.AccessDenied):
                        pass
            
        except psutil.NoSuchProcess:
            break
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            
        time.sleep(5)

# Thread management
_collection_thread = None
_thread_lock = threading.Lock()

def start_metrics_collection():
    """Start the metrics collection thread"""
    global _collection_thread
    
    with _thread_lock:
        if _collection_thread is None or not _collection_thread.is_alive():
            if not _metrics_initialized:
                initialize_metrics()
            _collection_thread = threading.Thread(target=collect_system_metrics, daemon=True)
            _collection_thread.start()
            print("Metrics collection thread started")
    
    return _collection_thread

def get_metrics_registry():
    """Get the metrics registry for use with Prometheus"""
    if not _metrics_initialized:
        initialize_metrics()
    return METRICS_REGISTRY