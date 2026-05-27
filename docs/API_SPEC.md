# API Specification Document

## Project
Intelligent Quality Platform (IQP)

---

# 1. Overview

This document defines the REST API specification for the Intelligent Quality Platform (IQP).

The APIs support:

- User authentication
- File ingestion
- MCP workflow execution
- Job monitoring
- Dashboard metrics

---

# 2. Base URL

```http
https://iqp.fngt.pro/api/v1
```

---

# 3. Authentication

## Authentication Method

The platform uses Bearer Token authentication.

### Example

```http
Authorization: Bearer <access_token>
```

---

# 4. Common Response Codes

| Status Code | Description |
|---|---|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

# 5. API Endpoints

---

# 5.1 Authentication APIs

## Login

### Endpoint

```http
POST /auth/login
```

### Description

Authenticate user and generate access token.

### Request Body

```json
{
  "username": "admin",
  "password": "password123"
}
```

### Response

```json
{
  "access_token": "jwt-token",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

## Logout

### Endpoint

```http
POST /auth/logout
```

### Description

Invalidate current user session.

### Headers

```http
Authorization: Bearer <access_token>
```

### Response

```json
{
  "message": "Logout successful"
}
```

---

# 5.2 User APIs

## Get Current User

### Endpoint

```http
GET /users/me
```

### Description

Retrieve current authenticated user information.

### Response

```json
{
  "user_id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "ADMIN"
}
```

---

# 5.3 Ingestion APIs

## Upload File

### Endpoint

```http
POST /ingestion/upload
```

### Description

Upload and start ingestion job.

### Headers

```http
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

### Request

| Field | Type | Required |
|---|---|---|
| file | binary | Yes |

### Response

```json
{
  "ingestion_id": 101,
  "status": "UPLOADED",
  "message": "File uploaded successfully"
}
```

---

## Get Ingestion Job Status

### Endpoint

```http
GET /ingestion/{ingestion_id}
```

### Description

Retrieve ingestion job details.

### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| ingestion_id | bigint | Ingestion job ID |

### Response

```json
{
  "ingestion_id": 101,
  "file_name": "sample.csv",
  "status": "COMPLETED",
  "uploaded_at": "2026-05-26T10:00:00Z",
  "completed_at": "2026-05-26T10:05:00Z"
}
```

---

## List Ingestion Jobs

### Endpoint

```http
GET /ingestion/jobs
```

### Description

Retrieve all ingestion jobs.

### Query Parameters

| Parameter | Type | Required |
|---|---|---|
| status | string | No |
| page | integer | No |
| size | integer | No |

### Response

```json
{
  "total": 100,
  "page": 1,
  "size": 10,
  "items": [
    {
      "ingestion_id": 101,
      "file_name": "sample.csv",
      "status": "COMPLETED"
    }
  ]
}
```

---

# 5.4 MCP APIs

## Execute MCP Workflow

### Endpoint

```http
POST /mcp/execute
```

### Description

Execute MCP workflow.

### Request Body

```json
{
  "workflow_id": 10,
  "input_data": {
    "dataset": "customer_data"
  }
}
```

### Response

```json
{
  "execution_id": 501,
  "status": "RUNNING",
  "message": "Workflow execution started"
}
```

---

## Get MCP Execution Status

### Endpoint

```http
GET /mcp/executions/{execution_id}
```

### Description

Retrieve MCP execution details.

### Response

```json
{
  "execution_id": 501,
  "workflow_id": 10,
  "status": "COMPLETED",
  "started_at": "2026-05-26T10:10:00Z",
  "completed_at": "2026-05-26T10:12:00Z"
}
```

---

## List MCP Executions

### Endpoint

```http
GET /mcp/executions
```

### Description

Retrieve MCP execution history.

### Response

```json
{
  "total": 20,
  "items": [
    {
      "execution_id": 501,
      "status": "COMPLETED"
    }
  ]
}
```

---

# 5.5 Dashboard APIs

## Get Dashboard Metrics

### Endpoint

```http
GET /dashboard/metrics
```

### Description

Retrieve system monitoring metrics.

### Response

```json
{
  "active_ingestion_jobs": 5,
  "active_mcp_executions": 3,
  "cpu_usage": "45%",
  "memory_usage": "60%"
}
```

---

# 6. Error Response Format

## Example

```json
{
  "error_code": "INVALID_REQUEST",
  "message": "Missing required field",
  "details": [
    "file is required"
  ]
}
```

---

# 7. Pagination Standard

## Query Parameters

| Parameter | Description |
|---|---|
| page | Current page number |
| size | Number of records per page |

---

# 8. Security Requirements

- All APIs must use HTTPS
- JWT token expiration required
- Sensitive data must be encrypted
- Audit logging enabled

---

# 9. Performance Requirements

| API | Expected Response Time |
|---|---|
| Login | < 3 seconds |
| Upload File | < 5 seconds |
| Dashboard Metrics | < 2 seconds |

---

# 10. Concurrency Requirements

## Ingestion

- Support at least 20 concurrent upload jobs

## MCP

- Support multiple concurrent workflow executions

---

# 11. Future Enhancements

- API versioning
- WebSocket notifications
- Bulk ingestion API
- Async job callbacks

---