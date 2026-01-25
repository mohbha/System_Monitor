# 🛡️ System Health Monitoring Agent

A lightweight, containerized system monitoring agent built with Python. It tracks real-time system metrics (CPU, Memory, Disk), exposes them via a REST API (including Prometheus format), and triggers alerts based on configurable thresholds.

**Built to demonstrate core DevOps competencies:** Observability, Containerization, Automation, and API Development.

---

## 🏗️ Architecture
The agent runs as a background service with two main threads:
1.  **Collector Thread:** Polls system metrics using `psutil`, handles log rotation, and evaluates alert rules.
2.  **API Thread:** Runs a Flask server to expose metrics to external dashboards (like Grafana).



## 🚀 Features
* **Real-time Monitoring:** Tracks CPU, RAM, and Disk usage.
* **Alerting Engine:** Configurable thresholds for automatic warnings.
* **REST API:** JSON endpoints for integration with 3rd party tools.
* **Prometheus Support:** Native endpoint for scraping metrics.
* **Dockerized:** Fully containerized for "write once, run anywhere" deployment.
* **Resilience:** Graceful signal handling (SIGTERM/SIGINT) and structured logging.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9
* **Libraries:** `psutil` (Metrics), `Flask` (API), `PyYAML` (Config)
* **Containerization:** Docker
* **OS:** Linux (Alpine/Slim)

---

## ⚡ Quick Start (Docker)
The easiest way to run the agent is via Docker.

1.  **Build the Image**
    ```bash
    docker build -t system-monitor .
    ```

2.  **Run the Container**
    ```bash
    docker run -d -p 5000:5000 --name my-monitor system-monitor
    ```

3.  **Check Health**
    Visit `http://localhost:5000/metrics` to see real-time data.

---

## 🔧 Local Development (Manual)
If you want to run it without Docker (e.g., on macOS/Linux directly):

1.  **Install Dependencies**
    ```bash
    pip3 install -r requirements.txt
    ```

2.  **Run the Agent**
    ```bash
    python3 main.py
    ```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check for load balancers. |
| `GET` | `/metrics` | Returns system stats in standard JSON. |
| `GET` | `/metrics/prometheus` | Returns stats in Prometheus/OpenMetrics text format. |

---

## ⚙️ Configuration
Modify `config.yaml` to tune behavior:

```yaml
system:
  update_interval: 5  # Seconds between checks

alerts:
  cpu_threshold: 80   # Percent
  memory_threshold: 80
  disk_threshold: 90