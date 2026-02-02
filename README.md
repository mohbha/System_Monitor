# 🛡️ System Health Monitoring Agent

![Architecture Diagram](Image/architecture_diagram.png)


A production-ready observability stack built from scratch. What started as a simple Python script is now a containerized microservices architecture integrated with Prometheus and Grafana for real-time visualization.

This project demonstrates the evolution from **coding** a solution to **architecting** a system.

---

## 🌟 Key Features

* **Real-time Metrics:** Custom Python agent polls CPU, Memory, and Disk usage using `psutil`.
* **Microservices Architecture:** Decoupled services for metric collection, storage, and visualization.
* **One-Command Deployment:** Entire stack spins up instantly with `docker-compose`.
* **Prometheus Integration:** Exposes metrics via a standard `/metrics/prometheus` endpoint.
* **Beautiful Visualization:** Includes a pre-configured connection to Grafana for professional dashboards.
* **Containerized:** Runs consistently on any machine with Docker installed.

## 🏗️ Architecture

The system is composed of three services running in a private Docker network:

1.  **Producer (`system-monitor`):** A Python/Flask app that collects system metrics and exposes them on an internal API port (8000), mapped to host port 8000.
2.  **Collector (`prometheus`):** A time-series database that automatically scrapes metrics from the Python app every 5 seconds via internal DNS (`http://system-monitor:8000`).
3.  **Viewer (`grafana`):** A visualization platform that queries Prometheus to build real-time dashboards, accessible on host port 3000.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Framework:** Flask
* **Libraries:** `psutil`, `prometheus_client`
* **Containerization:** Docker & Docker Compose
* **Monitoring:** Prometheus
* **Visualization:** Grafana

---

## 🚀 Getting Started

Get the entire stack running on your machine in under a minute.

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mohbha/System_Monitor.git
    cd System_Monitor
    ```

2.  **Start the stack:**
    This command will build the Python image and start all three containers in the background.
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the services:**
    * **Grafana Dashboard:** [http://localhost:3000](http://localhost:3000)
        * **Default Login:** `admin` / `admin` (skip password change for local dev).
    * **Prometheus Targets:** [http://localhost:9090/targets](http://localhost:9090/targets) (Verify the app is being scraped).
    * **Raw Metrics API:** [http://localhost:8000/metrics/prometheus](http://localhost:8000/metrics/prometheus)

4.  **Stop the stack:**
    ```bash
    docker-compose down
    ```

---

## 📊 Setting up the Dashboard

Once logged into Grafana:

1.  **Add Data Source:** Go to `Configuration` -> `Data Sources` -> `Add data source` -> `Prometheus`.
    * **URL:** `http://prometheus:9090` (Important: Use the container name, not localhost).
    * Click `Save & test`.

2.  **Create Dashboard:** Click `+` -> `Dashboard` -> `Add visualization`. Select the Prometheus data source.

3.  **Add Queries:**
    * **CPU Usage:** Use the metric `system_cpu_usage`.
    * **RAM Usage:** Use the metric `system_memory_usage_percent`.
    * **Disk Space:** Use `system_disk_usage_percent` and set the visualization type to "Gauge".

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.