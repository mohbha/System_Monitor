#!/usr/bin/env python3
import time
import sys
import signal
import logging
import yaml
from logging.handlers import RotatingFileHandler

# IMPORTS: Custom modules we built in previous phases
from collector import SystemCollector
from alerts import AlertSystem
from api import APIServer  # <--- New Import for Phase 4

class Service:
    def __init__(self, config_path="config.yaml"):
        self.running = True
        self.config = self.load_config(config_path)
        self.setup_logging()
        
        # 1. Initialize Collector (Phase 1)
        self.collector = SystemCollector()
        
        # 2. Initialize Alerter (Phase 3)
        self.alerter = AlertSystem(self.config)
        
        # 3. Initialize API (Phase 4)
        # We pass the collector reference so the API can fetch real-time data
        api_port = self.config.get('api', {}).get('port', 8000)
        self.api = APIServer(port=api_port, collector_ref=self.collector)

        # DevOps Requirement: Handle signals for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Config file '{path}' not found. Please create it first.")
            sys.exit(1)

    def setup_logging(self):
        log_cfg = self.config['logging']
        
        self.logger = logging.getLogger("SystemMonitor")
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate logs if the service restarts internal components
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # File Handler (Rotates logs)
        file_handler = RotatingFileHandler(
            self.config['system']['log_location'],
            maxBytes=log_cfg['max_bytes'],
            backupCount=log_cfg['backup_count']
        )
        
        # Console Handler (Stdout)
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def shutdown(self, signum, frame):
        """
        Catches Ctrl+C or Docker stop signals.
        """
        print("\n") # Newline for clean terminal output
        self.logger.info("Shutdown signal received. Cleaning up...")
        self.running = False

    def run(self):
        self.logger.info("Service started.")
        
        # --- Start the API Server in a background thread ---
        # This allows the loop below to keep running while the web server handles requests
        self.logger.info(f"Starting API Server on port {self.api.port}...")
        self.api.start_in_thread()
        # -------------------------------------------------

        interval = self.config['system']['update_interval']
        
        while self.running:
            try:
                # 1. Collect Data
                metrics = self.collector.collect_all()
                
                # 2. Log Summary
                self.logger.info(
                    f"CPU: {metrics['cpu']['usage_percent']}% | "
                    f"Mem: {metrics['memory']['percent']}% | "
                    f"Disk: {metrics['disk']['percent']}%"
                )
                
                # 3. Check Alerts
                self.alerter.check_cpu(metrics['cpu']['usage_percent'])
                self.alerter.check_memory(metrics['memory']['percent'])
                self.alerter.check_disk(metrics['disk']['percent'])
                
                # 4. Smart Sleep Loop
                # Checks if we need to quit every second, rather than blocking for the full interval
                for _ in range(interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(5) # Prevent CPU spiking if something is consistently failing
        
        self.logger.info("Service stopped gracefully.")

if __name__ == "__main__":
    agent = Service()
    agent.run()