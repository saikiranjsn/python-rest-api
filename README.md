# Flask REST API with CNCF Monitoring Stack

A comprehensive Flask REST API project with Prometheus, Grafana, and Locust for load testing and monitoring.

## Features

- **Flask REST API** with 6 endpoints
- **Prometheus** metrics collection
- **Grafana** dashboards for visualization
- **Locust** distributed load testing
- **Node Exporter** for system metrics
- **Docker Compose** orchestration

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Locust Load   │    │   Grafana       │
│   Testing       │    │   Dashboard     │
│                 │    │   (Port 3000)   │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────────┐
          │   Prometheus        │
          │   Metrics           │
          │   (Port 9090)       │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │   Flask API         │
          │   (Port 5000)       │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │   Node Exporter     │
          │   System Metrics    │
          │   (Port 9100)       │
          └─────────────────────┘
```

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd /home/sai/Desktop/python-rest-api
   ```

2. **Start the monitoring stack:**
   ```bash
   docker compose up -d
   ```

3. **Access the services:**
   - **Flask API**: http://localhost:5000
   - **Rust API**: http://localhost:5001
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Prometheus**: http://localhost:9090
   - **Locust**: http://localhost:8089

## Rust API

The Rust version exposes the same API contract as the Flask app on port `5001`.

Use `http://rust-app:5000` as the host in the Locust UI when testing from the container network.

## API Endpoints

### Health Check
- **GET** `/api/health` - Check server status
- **GET** `/metrics` - Prometheus metrics endpoint

### Items API
- **GET** `/api/items` - Get all items
- **GET** `/api/items/<id>` - Get item by ID
- **POST** `/api/items` - Create new item

### Hello API
- **GET** `/api/hello?name=YourName` - Greeting endpoint

## Load Testing with Locust

1. **Access Locust Web UI**: http://localhost:8089

2. **Configure Load Test:**
   - **Number of users**: Start with 10, increase gradually
   - **Spawn rate**: 1 user/second
   - **Host**: `http://flask-app:5000` for Python or `http://rust-app:5000` for Rust

3. **Test Scenarios:**
   - Health checks (30% of requests)
   - Get items (40% of requests)
   - Hello endpoint (20% of requests)
   - Get item by ID (10% of requests)
   - Create item (10% of requests)

## Monitoring Dashboard

### Grafana Dashboards
Access http://localhost:3000 and login with admin/admin.

**Available Panels:**
- API Response Times
- Request Rate per Endpoint
- CPU Usage %
- Memory Usage %
- HTTP Status Code Distribution
- Active Locust Users
- Locust Response Times
- Requests Per Second (RPS)

### Prometheus Metrics
- Flask HTTP request metrics
- System CPU/Memory usage
- Locust load testing metrics

## Load Testing Scenarios

### Light Load (10 users)
```bash
# In Locust UI: Set 10 users, spawn rate 1
# Monitor response times should be < 100ms
```

### Medium Load (50 users)
```bash
# In Locust UI: Set 50 users, spawn rate 5
# Monitor CPU usage and response times
```

### Heavy Load (100+ users)
```bash
# In Locust UI: Set 100+ users, spawn rate 10
# Watch for performance degradation
```

## Troubleshooting

### Services Not Starting
```bash
# Check logs
docker compose logs

# Restart services
docker compose restart
```

### High Resource Usage
```bash
# Monitor with htop
htop

# Check Docker stats
docker stats
```

### Locust Connection Issues
```bash
# Ensure Flask app is running
curl http://localhost:5000/api/health

# Check Locust logs
docker compose logs locust-master
```

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Run with Docker
docker compose up flask-app
```

### Adding New Metrics
```python
from prometheus_flask_exporter import Counter

custom_counter = Counter('custom_requests', 'Description of counter')
custom_counter.inc()  # Increment counter
```

## Cleanup

```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: deletes data)
docker compose down -v
```

## Project Structure

```
.
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Flask app container
├── docker-compose.yml       # Service orchestration
├── load_test/
│   └── locustfile.py        # Load testing scenarios
├── monitoring/
│   ├── prometheus.yml       # Prometheus configuration
│   └── grafana/
│       ├── dashboards/
│       │   └── flask-load-test.json
│       └── provisioning/
│           ├── dashboards/
│           └── datasources/
└── README.md
```

## License

MIT
