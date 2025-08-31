# stackit-api-assessment

This is a **minimal RESTful web service** that receives notifications via a `POST` request and forwards them to a Slack channel using an incoming webhook based on their type.

- Notifications of type **`Warning`** → ✅ Forwarded to Slack.  
- Notifications of type **`Info`** → ❌ Ignored.  

The service also stores received notifications **in memory** so they can be retrieved later via a `GET` request.

---

## 🚀 Features
- Simple REST API with Flask
- Forwards notifications of type `Warning` to Slack
- Stores notifications in-memory (no database required)
- Dockerized for easy setup
- `.env` file support for sensitive information (Slack webhook URL)
- Thoughtful design for multi-service usage and production readiness

---

## 📂 Project Structure
```
stackit-api-assessment/
│── app.py               # Main Flask application
│── requirements.txt     # Python dependencies
│── Dockerfile           # Docker build file
│── docker-compose.yml   # Docker Compose config
│── .env                 # Environment variables (not committed to git)
│── README.md            # Documentation
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/NarcisseObadiah/stackit-api-assessment.git
cd stackit-api-assessment/
```

### 2. Create a `.env` file
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

### 3. Build and run with Docker
```bash
docker-compose up --build
```

The API will be available at:  
👉 `http://localhost:5000`

---

## 📡 API Endpoints

### POST `/notify`
Send a notification to the API.

**Request Example**
```bash
curl -X POST http://localhost:5000/notify \
  -H "Content-Type: application/json" \
  -d '{
        "Type": "Warning",
        "Name": "Backup Failure",
        "Description": "The backup failed due to a database problem"
      }'
```

- `"Warning"` → forwarded to Slack  
- `"Info"` → stored but **not forwarded**  

**Response Example**
```json
{
  "status": "forwarded",
  "message": "Notification forwarded to Slack"
}
```

---

### GET `/notifications`
Retrieve all notifications stored in memory.

**Request Example**
```bash
curl http://localhost:5000/notifications
```

**Response Example**
```json
[
  {
    "Type": "Warning",
    "Name": "Backup Failure",
    "Description": "The backup failed due to a database problem"
  },
  {
    "Type": "Info",
    "Name": "Quota Exceeded",
    "Description": "Compute Quota exceeded"
  }
]
```

---

## 🔗 Multi-Service Usage

The API is designed so **different services** in an organization can push notifications without managing Slack integration themselves.  

Example scenario:
- A **backup service** sends `POST /notify` on failures.  
- A **monitoring service** sends quota alerts or CPU usage events.  
- A **deployment service** notifies about failed pipelines.  

Each service just calls the **same `/notify` endpoint**, letting the API handle:
- Filtering (`Warning` only forwarded)  
- Forwarding to Slack  
- Storing in-memory for visibility  

This approach **centralizes notification management** and makes the API easy for multiple consumers.

---

## ⚡ Asynchronous Considerations

Currently, Slack forwarding is synchronous. In a **production scenario**:

- Multiple services might send high volumes of notifications concurrently.  
- Forwarding to Slack could take 100–500ms per request.  
- Using **asynchronous HTTP calls** (`aiohttp` or `httpx`) would allow the API to respond immediately while sending messages concurrently.  

This improves **throughput, reduces latency**, and scales better under load.

---

## 📦 Potential Production Deployment (Kubernetes)

In a production environment, this API could be deployed as follows:

1. **Containerized** (already Dockerized)
2. **Kubernetes Deployment** with multiple replicas for **high availability**
3. **Secrets management** for Slack webhook using Kubernetes Secrets
4. **Service** (ClusterIP or LoadBalancer) to expose the API
5. **Horizontal Pod Autoscaler** to handle traffic spikes
6. **Monitoring & Logging** (Prometheus/Grafana) to track requests, forwarding success, and latency

> This ensures scalability, maintainability, and robustness.

---

## 📝 API Documentation / Swagger

For this coding challenge, the API is documented in this README with example requests.  

In a **real production environment**, I would add **Swagger / OpenAPI** to:
- Automatically generate interactive docs  
- Help multiple teams consume the API  
- Ensure consistency and maintainability  

Flask supports Swagger via:
- [flasgger](https://github.com/flasgger/flasgger)  
- [flask-swagger-ui](https://github.com/swagger-api/swagger-ui)

---

## 🧪 Testing

- Use `curl` or Postman to test POST/GET endpoints  
- In production, add automated tests with `pytest` to ensure reliability  

---

## 🛠️ Requirements

- Python 3.11  
- Flask  
- Requests library  

(Installed via `requirements.txt`)

