# Entity Relationship Diagram (ERD)

## Project
Intelligent Quality Platform (IQP)

---

# 1. Overview

This document describes the database entities and relationships for the Intelligent Quality Platform (IQP).

The system supports:

- User authentication
- File ingestion
- MCP workflow execution
- Job monitoring
- Audit logging

---

# 2. ERD Diagram

```mermaid
erDiagram

    USERS {
        bigint user_id PK
        varchar username
        varchar password_hash
        varchar email
        varchar role
        timestamp created_at
        timestamp updated_at
    }

    INGESTION_JOBS {
        bigint ingestion_id PK
        bigint user_id FK
        varchar file_name
        varchar file_type
        varchar status
        bigint file_size
        timestamp uploaded_at
        timestamp completed_at
    }

    MCP_WORKFLOWS {
        bigint workflow_id PK
        varchar workflow_name
        varchar description
        varchar status
        timestamp created_at
    }

    MCP_EXECUTIONS {
        bigint execution_id PK
        bigint workflow_id FK
        bigint user_id FK
        varchar execution_status
        timestamp started_at
        timestamp completed_at
        text execution_log
    }

    SYSTEM_LOGS {
        bigint log_id PK
        bigint user_id FK
        varchar module_name
        varchar log_level
        text message
        timestamp created_at
    }

    DASHBOARD_METRICS {
        bigint metric_id PK
        varchar metric_name
        varchar metric_value
        timestamp collected_at
    }

    USERS ||--o{ INGESTION_JOBS : uploads
    USERS ||--o{ MCP_EXECUTIONS : executes
    USERS ||--o{ SYSTEM_LOGS : generates

    MCP_WORKFLOWS ||--o{ MCP_EXECUTIONS : contains


    