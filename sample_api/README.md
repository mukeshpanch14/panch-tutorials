# Sample API

A simple FastAPI application with GET, POST, PUT endpoints and a health check endpoint, designed for testing purposes.

## Features

- **Health Check**: `GET /health` - Simple endpoint to check API status
- **GET Endpoint**: `GET /items/{item_id}` - Retrieves item with optional query parameters
- **POST Endpoint**: `POST /items` - Creates a new item with JSON payload
- **PUT Endpoint**: `PUT /items/{item_id}` - Updates an item with JSON payload

## Quick Start

### Using Docker (Recommended)

1. Build the Docker image locally:
```bash
docker build -t sample-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 sample-api
```

3. Access the API:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

### Using Pre-built Docker Image (Fallback)

As a fallback option, you can use the pre-built Docker image:

1. Pull the Docker image from Docker Hub:
```bash
docker pull mukeshpanch14/panchrepo:sample-api-latest
```

2. Run the container:
```bash
docker run -p 8000:8000 mukeshpanch14/panchrepo:sample-api-latest
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

### Get Item
```bash
GET /items/{item_id}?skip=0&limit=10
```
**Parameters:**
- `item_id` (path): Item identifier
- `skip` (query, optional): Number of items to skip (default: 0)
- `limit` (query, optional): Maximum number of items (default: 10, max: 100)

**Response:**
```json
{
  "item_id": "123",
  "skip": 0,
  "limit": 10,
  "message": "GET request processed successfully"
}
```

### Create Item
```bash
POST /items
Content-Type: application/json

{
  "name": "Sample Item",
  "description": "This is a test item"
}
```

**Response:**
```json
{
  "item_id": "new_item",
  "name": "Sample Item",
  "description": "This is a test item",
  "message": "POST request processed successfully"
}
```

### Update Item
```bash
PUT /items/{item_id}
Content-Type: application/json

{
  "name": "Updated Item",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "item_id": "123",
  "name": "Updated Item",
  "description": "Updated description",
  "message": "PUT request processed successfully"
}
```

## Example API Calls

### Using curl

**Health Check:**
```bash
curl http://localhost:8000/health
```

**GET Item:**
```bash
curl http://localhost:8000/items/123?skip=0&limit=10
```

**POST Item:**
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Test description"}'
```

**PUT Item:**
```bash
curl -X PUT http://localhost:8000/items/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "description": "Updated description"}'
```

## Docker Development

For development with volume mounting:

```bash
docker run -p 8000:8000 -v $(pwd)/app:/app/app sample-api
```

## Notes

- All endpoints are designed for testing purposes and will echo back received data
- The API uses FastAPI's automatic interactive documentation available at `/docs`
- The Docker image runs as a non-root user for security best practices

