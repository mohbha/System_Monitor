import logging
import os

# Optional: Import smtplib for email or requests for Slack if you want to go advanced later
# import smtplib
# import requests

class AlertSystem:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("SystemMonitor")
    
    def check_cpu(self, usage):
        threshold = self.config['alerts']['cpu_threshold']
        if usage > threshold:
            self.trigger_alert(f"HIGH CPU USAGE DETECTED: {usage}% (Threshold: {threshold}%)")

    def check_memory(self, usage):
        threshold = self.config['alerts']['memory_threshold']
        if usage > threshold:
            self.trigger_alert(f"HIGH MEMORY USAGE DETECTED: {usage}% (Threshold: {threshold}%)")

    def check_disk(self, usage):
        threshold = self.config['alerts']['disk_threshold']
        if usage > threshold:
            self.trigger_alert(f"LOW DISK SPACE: Usage is at {usage}% (Threshold: {threshold}%)")

    def trigger_alert(self, message):
        """
        Handles the delivery of the alert.
        """
        # 1. Log it as a WARNING (so it stands out in logs)
        self.logger.warning(message)
        
        # 2. (Optional) Print to console with color for visibility during local testing
        # \033[91m is the ANSI escape code for Red text on Mac/Linux terminals
        print(f"\033[91m[ALERT] {message}\033[0m")

        # 3. Real-world Notification integrations would go here:
        if self.config['alerts'].get('enable_slack'):
            self.send_slack_alert(message)
            
    def send_slack_alert(self, message):
        # SECURITY NOTE: Never hardcode webhooks!
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook_url:
            self.logger.error("Slack enabled but SLACK_WEBHOOK_URL not set.")
            return
        
        # Logic to post to Slack would go here...
        # requests.post(webhook_url, json={"text": message})