import os
import platform
import time
import psutil

def system_metrics():
    disk_path = os.path.abspath(os.sep)
    disk = psutil.disk_usage(disk_path)
    net = psutil.net_io_counters()
    return {
        "hostname": platform.node(),
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / 1024**3, 2),
        "disk_total_gb": round(disk.total / 1024**3, 2),
        "network_sent_mb": round(net.bytes_sent / 1024**2, 2),
        "network_recv_mb": round(net.bytes_recv / 1024**2, 2),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "process_count": len(psutil.pids()),
    }
