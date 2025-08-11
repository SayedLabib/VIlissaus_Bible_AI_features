# 🙏 Vilisasu Bible AI

An AI-powered Bible chat service that provides biblical guidance, answers questions, generates prayers, and compares different Bible versions using OpenAI's GPT models.

## ✨ Features

- **Biblical Q&A**: Ask any question about the Bible and get comprehensive answers
- **Prayer Generation**: Generate personalized prayers based on biblical principles
- **Version Comparison**: Compare verses across KJV, NIV, ESV, and NLT translations
- **Contradiction Acknowledgment**: Honest handling of biblical contradictions and different interpretations
- **Scriptural References**: All responses include relevant Bible verse citations
- **RESTful API**: Simple HTTP API for easy integration
- **Docker Support**: Containerized deployment with Nginx reverse proxy
- **Rate Limiting**: Built-in API rate limiting for stability
- **Health Monitoring**: Comprehensive health checks and monitoring

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### 1. Clone & Configure

```bash
git clone <repository-url>
cd Vilisasu_Bible_AI

# Copy and configure environment file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Deploy

```bash
# Stop any running containers
docker-compose down

# Build and start services
docker-compose build
docker-compose up -d
```

### 3. Test

The service will be available at:
- **Main API**: http://localhost
- **Documentation**: http://localhost/docs
- **Health Check**: http://localhost/health

## 📖 API Usage

### Bible Chat Endpoint

**POST** `/api/v1/bible-chat/query`

```bash
curl -X POST http://localhost/api/v1/bible-chat/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What does the Bible say about love?"}'
```

**Request Schema:**
```json
{
  "query": "Your Bible-related question here"
}
```

**Response Schema:**
```json
{
  "success": true,
  "response": "The Bible teaches about love in many beautiful passages...",
  "timestamp": "2025-07-21T10:30:00"
}
```

### Example Queries

#### Biblical Questions
```json
{"query": "What does the Bible say about forgiveness?"}
{"query": "Who wrote the book of Romans?"}
{"query": "What is the Gospel according to John?"}
```

#### Prayer Requests
```json
{"query": "Can you generate a prayer for healing?"}
{"query": "Write a prayer of thanksgiving"}
{"query": "Create a prayer for wisdom and guidance"}
```

#### Version Comparisons
```json
{"query": "Compare John 3:16 in KJV, NIV, ESV, and NLT"}
{"query": "Show me Psalm 23 in different translations"}
```

#### Theological Questions
```json
{"query": "Are there contradictions in the Bible?"}
{"query": "What are different Christian views on baptism?"}
{"query": "Explain the Trinity from a biblical perspective"}
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Client      │───▶│      Nginx      │───▶│   FastAPI App   │
│                 │    │  Reverse Proxy  │    │   (Bible AI)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   OpenAI API    │
                                               │      GPT-4      │
                                               └─────────────────┘
```

### Components

- **FastAPI Application**: Main Bible AI service
- **Nginx**: Reverse proxy with rate limiting and CORS
- **Redis**: Caching layer (optional)
- **OpenAI API**: AI model for biblical responses

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPEN_AI_API_KEY="your-api-key"
export Model="gpt-4o-2024-08-06"

# Run locally
cd app
python main.py
```

### Project Structure

```
Vilisasu_Bible_AI/
├── app/
│   ├── main.py                 # FastAPI application
│   └── services/
│       ├── api_manager/
│       │   └── Bible_Chat_api_manager.py
│       └── Bible_Chat_Service/
│           ├── Bible_chat_schema.py
│           ├── Bible_chat_service.py
│           └── Bible_chat_route.py
├── nginx/
│   └── nginx.conf              # Nginx configuration
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Application container
└── requirements.txt            # Python dependencies
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPEN_AI_API_KEY` | OpenAI API key | Required |
| `Model` | OpenAI model name | `gpt-4o-2024-08-06` |
| `PORT` | Application port | `8000` |
| `ENVIRONMENT` | Environment mode | `production` |
| `DEBUG` | Debug mode | `False` |

### Docker Compose Services

- **bible-ai-app**: Main FastAPI application
- **nginx**: Reverse proxy and load balancer
- **redis**: Caching and session storage

## 📊 Health Checks

### Health Endpoints

- **Application**: `GET /health`
- **Bible Chat Service**: `GET /api/v1/bible-chat/health`
- **Nginx**: `GET /nginx-health`

## 🚢 Deployment

### Production Deployment

1. **Update Environment**:
   ```bash
   # In .env file
   ENVIRONMENT=production
   DEBUG=False
   ```

2. **Enable SSL** (recommended):
   - Uncomment SSL configuration in `nginx/nginx.conf`
   - Add SSL certificates to `ssl/` directory
   - Update docker-compose.yml volume mounts

3. **Scale Services**:
   ```bash
   docker-compose up -d --scale bible-ai-app=3
   ```

### Cloud Deployment

The application is ready for deployment on:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **Kubernetes clusters**

## 🔒 Security

- ✅ Non-root container user
- ✅ Rate limiting on API endpoints
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ Health checks and monitoring
- ✅ Resource limits on containers
- ⚠️ Add SSL certificates for HTTPS
- ⚠️ Configure firewall rules
- ⚠️ Set up proper secret management

## 🤝 API Integration

### Python Example

```python
import requests

def ask_bible_question(question):
    response = requests.post(
        "http://localhost/api/v1/bible-chat/query",
        json={"query": question}
    )
    return response.json()

# Usage
result = ask_bible_question("What does the Bible say about hope?")
print(result["response"])
```

### JavaScript Example

```javascript
async function askBibleQuestion(question) {
    const response = await fetch('/api/v1/bible-chat/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: question })
    });
    return await response.json();
}

// Usage
askBibleQuestion("What does the Bible say about peace?")
    .then(result => console.log(result.response));
```

## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**:
   ```bash
   # Check .env file
   cat .env | grep OPEN_AI_API_KEY
   ```

2. **Service Not Starting**:
   ```bash
   # Check logs
   docker-compose logs -f bible-ai-app
   ```

3. **Connection Refused**:
   ```bash
   # Check if services are running
   docker-compose ps
   ```

4. **Memory Issues**:
   ```bash
   # Check resource usage
   docker stats
   ```

### Support Commands

```bash
# View all logs
docker-compose logs -f

# Restart specific service
docker-compose restart bible-ai-app

# Check service health
curl http://localhost/health

# Test API endpoint
curl -X POST http://localhost/api/v1/bible-chat/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- FastAPI for the excellent web framework
- The biblical scholars and translators of KJV, NIV, ESV, and NLT

---

**Built with ❤️ for biblical study and spiritual guidance**
