import psutil
import time
import json
import os

class SystemCollector:
    def __init__(self):
        # Determine the host operating system
        self.os_type = os.name

    def get_cpu_metrics(self):
        """
        Returns CPU usage percentage and frequency.
        """
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "core_usage": psutil.cpu_percent(interval=1, percpu=True),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }

    def get_memory_metrics(self):
        """
        Returns total, available, and used memory in MB.
        """
        mem = psutil.virtual_memory()
        return {
            "total_mb": mem.total // (1024 * 1024),
            "available_mb": mem.available // (1024 * 1024),
            "used_mb": mem.used // (1024 * 1024),
            "percent": mem.percent
        }

    def get_disk_metrics(self):
        """
        Returns disk usage for the root partition.
        """
        disk = psutil.disk_usage('/')
        return {
            "total_gb": disk.total // (1024 * 1024 * 1024),
            "used_gb": disk.used // (1024 * 1024 * 1024),
            "free_gb": disk.free // (1024 * 1024 * 1024),
            "percent": disk.percent
        }

    def collect_all(self):
        """
        Aggregates all metrics into a single dictionary with a timestamp.
        """
        return {
            "timestamp": time.time(),
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "disk": self.get_disk_metrics()
        }

if __name__ == "__main__":
    # Test the collector
    collector = SystemCollector()
    metrics = collector.collect_all()
    
    # Print as pretty JSON to verify
    print(json.dumps(metrics, indent=4))