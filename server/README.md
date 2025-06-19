# Mem0 Server

A REST API server for the Mem0 memory management system.

## Features

- Memory storage and retrieval
- Search functionality
- Memory history tracking
- API key authentication (optional)

## Environment Variables

Create a `.env` file in the server directory with the following variables:

```env
# API Authentication (optional)
# If API_KEY is set, all requests must include Authorization header with Bearer token
API_KEY=your_api_key_here

# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_COLLECTION_NAME=memories

# Neo4j Configuration
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=mem0graph

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# History Database Path
HISTORY_DB_PATH=/app/history/history.db
```

## API Authentication

如果设置了 `API_KEY` 环境变量，所有API请求都需要在请求头中包含授权信息：

```
Authorization: Bearer your_api_key_here
```

如果没有设置 `API_KEY`，则无需认证即可访问所有API端点。

### 认证错误

- 如果设置了API_KEY但请求中没有Authorization头：返回401状态码，错误信息："Authorization header required"
- 如果Authorization头中的API_KEY不匹配：返回401状态码，错误信息："Invalid API Key"

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

启动服务器后，访问 http://localhost:8000/docs 查看自动生成的API文档。
