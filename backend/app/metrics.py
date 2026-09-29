from prometheus_client import Gauge

cpu_gauge = Gauge("linuxops_cpu_percent", "Current CPU utilization")
memory_gauge = Gauge("linuxops_memory_percent", "Current memory utilization")
disk_gauge = Gauge("linuxops_disk_percent", "Current root disk utilization")

def update_metrics(data):
    cpu_gauge.set(data["cpu_percent"])
    memory_gauge.set(data["memory_percent"])
    disk_gauge.set(data["disk_percent"])
