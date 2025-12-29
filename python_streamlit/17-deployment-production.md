# Deployment and Production - Deep Dive

## Overview

This guide covers deploying Streamlit applications to various platforms including Streamlit Cloud, Heroku, Docker, AWS, Azure, and Google Cloud, along with environment variables, production best practices, and monitoring.

## Streamlit Cloud Deployment

### Getting Started

1. **Push to GitHub**: Push your app to a GitHub repository
2. **Sign up**: Go to [share.streamlit.io](https://share.streamlit.io)
3. **Deploy**: Click "New app" and connect your repository

### Requirements

- `requirements.txt` file in your repository
- Main app file (e.g., `app.py`)
- GitHub repository (public or private with Streamlit Cloud access)

### Example requirements.txt

```txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
```

### Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
```

## Deploying to Heroku

### Setup

1. **Install Heroku CLI**: [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)
2. **Create Procfile**:

```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Create setup.sh**:

```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

4. **Deploy**:

```bash
heroku create your-app-name
git push heroku main
```

## Docker Containerization

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./app:/app
    environment:
      - STREAMLIT_SERVER_PORT=8501
```

### Build and Run

```bash
# Build image
docker build -t streamlit-app .

# Run container
docker run -p 8501:8501 streamlit-app

# With docker-compose
docker-compose up
```

## AWS Deployment

### EC2 Deployment

1. **Launch EC2 instance**: Ubuntu or Amazon Linux
2. **Install dependencies**:

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install streamlit pandas
```

3. **Run app**:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

4. **Configure security group**: Allow port 8501

### ECS Deployment

1. **Create Docker image**: Push to ECR
2. **Create ECS task definition**:

```json
{
  "family": "streamlit-app",
  "containerDefinitions": [{
    "name": "streamlit",
    "image": "your-ecr-repo/streamlit-app",
    "portMappings": [{
      "containerPort": 8501
    }]
  }]
}
```

3. **Create ECS service**: Deploy task definition

### App Runner Deployment

1. **Push to GitHub**: Connect repository
2. **Create App Runner service**: Configure build and run commands
3. **Deploy**: App Runner handles deployment automatically

## Azure Deployment

### Azure App Service

1. **Create App Service**: Choose Python runtime
2. **Configure startup command**:

```
pip install -r requirements.txt && streamlit run app.py --server.port=8000 --server.address=0.0.0.0
```

3. **Deploy**: Use Azure CLI or GitHub Actions

### Azure Container Instances

1. **Build Docker image**: Push to Azure Container Registry
2. **Create container instance**:

```bash
az container create \
  --resource-group myResourceGroup \
  --name streamlit-app \
  --image myregistry.azurecr.io/streamlit-app \
  --dns-name-label streamlit-app \
  --ports 8501
```

## Google Cloud Deployment

### Cloud Run

1. **Build container**:

```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/streamlit-app
```

2. **Deploy**:

```bash
gcloud run deploy streamlit-app \
  --image gcr.io/PROJECT-ID/streamlit-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### App Engine

1. **Create app.yaml**:

```yaml
runtime: python39

entrypoint: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

env_variables:
  STREAMLIT_SERVER_PORT: 8080
```

2. **Deploy**:

```bash
gcloud app deploy
```

## Environment Variables and Secrets

### Setting Environment Variables

#### Streamlit Cloud

1. Go to app settings
2. Click "Secrets"
3. Add secrets in TOML format:

```toml
[secrets]
DATABASE_URL = "postgresql://..."
API_KEY = "your-api-key"
```

#### Heroku

```bash
heroku config:set DATABASE_URL=postgresql://...
heroku config:set API_KEY=your-api-key
```

#### Docker

```bash
docker run -e DATABASE_URL=postgresql://... streamlit-app
```

### Using Secrets in App

```python
import streamlit as st
import os

# From environment variables
database_url = os.getenv("DATABASE_URL")

# From Streamlit secrets
if "secrets" in st.secrets:
    api_key = st.secrets["API_KEY"]
```

## Production Best Practices

### 1. Security

```python
import streamlit as st

# Don't expose secrets
# Bad
st.write(f"API Key: {api_key}")

# Good
if st.checkbox("Show API status"):
    st.write("API is connected")
```

### 2. Error Handling

```python
import streamlit as st
import logging

logger = logging.getLogger(__name__)

try:
    # Your code
    result = process_data()
except Exception as e:
    logger.error(f"Error: {str(e)}", exc_info=True)
    st.error("An error occurred. Please try again.")
```

### 3. Performance

```python
import streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    # Expensive operation
    return process_data()

# Use caching for expensive operations
data = load_data()
```

### 4. Monitoring

```python
import streamlit as st
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Log app usage
def log_usage(action):
    logger.info(f"{datetime.now()}: {action}")

# Use in app
if st.button("Process"):
    log_usage("Process button clicked")
    # Process data
```

## Monitoring and Logging

### Application Logs

```python
import streamlit as st
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log important events
logger.info("App started")
logger.warning("Low memory")
logger.error("Error occurred")
```

### Health Checks

```python
import streamlit as st
import requests

def health_check():
    try:
        # Check database
        # Check API
        return True
    except:
        return False

if not health_check():
    st.error("Service unavailable")
```

### Metrics

```python
import streamlit as st
from datetime import datetime

# Track usage
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

st.session_state.usage_count += 1

# Log metrics
logger.info(f"Usage count: {st.session_state.usage_count}")
```

## Practical Examples

### Example 1: Production-Ready App

```python
import streamlit as st
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Production App",
    page_icon="🚀",
    layout="wide"
)

# Environment variables
API_KEY = os.getenv("API_KEY", "default-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Error handling
try:
    # App code
    st.title("Production App")
    
    if DEBUG:
        st.sidebar.write("Debug Mode Enabled")
        st.sidebar.write(f"API Key: {API_KEY[:10]}...")
    
    # Main app logic
    st.write("App is running!")
    
except Exception as e:
    logger.error(f"Error: {str(e)}", exc_info=True)
    st.error("An error occurred. Please contact support.")
```

### Example 2: Docker Deployment Setup

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create streamlit config
RUN mkdir -p ~/.streamlit
RUN echo "[server]\nheadless = true\nport = 8501\n" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Best Practices

1. **Use environment variables**: Don't hardcode secrets
2. **Enable logging**: Log important events
3. **Handle errors**: Graceful error handling
4. **Monitor performance**: Track app usage
5. **Test deployment**: Test in staging first

## Common Pitfalls

### Pitfall 1: Exposing Secrets

**Problem:**
```python
st.write(f"API Key: {api_key}")  # Exposed in UI!
```

**Solution:**
```python
# Use environment variables
api_key = os.getenv("API_KEY")
# Never display in UI
```

### Pitfall 2: Not Setting Port

**Problem:**
```dockerfile
CMD ["streamlit", "run", "app.py"]  # Wrong port!
```

**Solution:**
```dockerfile
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
```

## Next Steps

Now that you can deploy apps:

- [External Integrations](./18-external-integrations.md) - Connect to external services
- [Best Practices](./19-best-practices.md) - More deployment tips

## References

- [Streamlit Cloud](https://streamlit.io/cloud)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [AWS Documentation](https://aws.amazon.com/documentation/)

