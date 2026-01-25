from flask import Flask, jsonify, Response
import threading

class APIServer:
    def __init__(self, host='0.0.0.0', port=8000, collector_ref=None):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.collector = collector_ref # Reference to the collector to get real-time data

        # Define Routes
        self.app.add_url_rule('/', 'health', self.health_check)
        self.app.add_url_rule('/metrics', 'metrics', self.get_metrics)
        self.app.add_url_rule('/metrics/prometheus', 'prometheus', self.get_prometheus_metrics)

    def health_check(self):
        """Simple health check for Docker/K8s liveness probes."""
        return jsonify({"status": "healthy", "service": "system-monitor-agent"})

    def get_metrics(self):
        """Return metrics in standard JSON format."""
        if self.collector:
            # We fetch the latest data directly from the collector
            data = self.collector.collect_all()
            return jsonify(data)
        return jsonify({"error": "Collector not initialized"}), 500

    def get_prometheus_metrics(self):
        """
        Return metrics in Prometheus text format.
        This is what tools like Grafana/Prometheus look for.
        """
        if not self.collector:
            return "Error: Collector not found", 500

        data = self.collector.collect_all()
        
        # Format: metric_name value
        response_lines = [
            "# HELP system_cpu_usage CPU usage percentage",
            "# TYPE system_cpu_usage gauge",
            f"system_cpu_usage {data['cpu']['usage_percent']}",
            
            "# HELP system_memory_usage_percent Memory usage percentage",
            "# TYPE system_memory_usage_percent gauge",
            f"system_memory_usage_percent {data['memory']['percent']}",
            
            "# HELP system_disk_usage_percent Disk usage percentage",
            "# TYPE system_disk_usage_percent gauge",
            f"system_disk_usage_percent {data['disk']['percent']}"
        ]
        
        return Response("\n".join(response_lines), mimetype="text/plain")

    def run(self):
        # We disable the default Flask banner to keep logs clean
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def start_in_thread(self):
        """Helper to run Flask in a separate thread so it doesn't block the main loop."""
        thread = threading.Thread(target=self.run)
        thread.daemon = True # Thread dies if main program dies
        thread.start()