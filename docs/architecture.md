# Architecture Overview

## System Design

The AI-Powered Shopify Analytics App follows a microservices architecture with clear separation of concerns:

### Components

#### 1. Rails API Gateway
**Responsibilities:**
- Handle HTTP requests from clients
- Validate input and authenticate requests
- Manage Shopify OAuth flow
- Store request logs and metadata
- Forward questions to Python AI service
- Format and return responses

**Technology:**
- Ruby on Rails 7.x (API-only)
- PostgreSQL for data persistence
- Redis for session management

#### 2. Python AI Service
**Responsibilities:**
- Process natural language questions
- Orchestrate LLM-powered agent workflow
- Generate ShopifyQL queries
- Execute queries against Shopify API
- Convert technical results to business insights

**Technology:**
- FastAPI for high-performance API
- LangChain for LLM orchestration
- OpenAI GPT-4 for language understanding
- Redis for caching

#### 3. Shopify Integration Layer
**Responsibilities:**
- OAuth authentication
- API request management
- Rate limiting compliance
- Data transformation

## Data Flow

```
1. Client Request
   ↓
2. Rails API Gateway
   - Validates request
   - Checks store authentication
   - Logs request
   ↓
3. Python AI Service
   - Classifies intent
   - Generates ShopifyQL
   - Executes query
   - Explains results
   ↓
4. Shopify API
   - Returns raw data
   ↓
5. Response Pipeline
   - Python processes data
   - Rails formats response
   - Client receives answer
```

## Agent Architecture

### Agentic Workflow

The Python AI service implements a multi-step agentic workflow:

#### Step 1: Intent Classification
- **Input:** Natural language question
- **Process:** LLM analyzes question to extract:
  - Domain (orders, products, inventory, customers)
  - Metrics needed (count, sum, average)
  - Time period (last week, next month)
  - Filters and conditions
- **Output:** Structured intent object

#### Step 2: Query Planning
- **Input:** Intent object
- **Process:** Agent decides:
  - Which Shopify data sources to query
  - What fields are required
  - How to structure the query
- **Output:** Query plan

#### Step 3: ShopifyQL Generation
- **Input:** Query plan
- **Process:** LLM generates syntactically correct ShopifyQL
- **Validation:** Query validator checks for:
  - Valid syntax
  - Allowed operations (read-only)
  - Proper table references
- **Output:** Validated ShopifyQL query

#### Step 4: Execution & Validation
- **Input:** ShopifyQL query
- **Process:**
  - Check cache for recent results
  - Execute against Shopify API
  - Handle errors and empty results
  - Validate data quality
- **Output:** Raw data from Shopify

#### Step 5: Result Explanation
- **Input:** Raw data + original question
- **Process:** LLM converts technical data to:
  - Business-friendly language
  - Actionable recommendations
  - Confidence assessment
- **Output:** Human-readable answer

## Database Schema

### Rails Database (PostgreSQL)

#### stores
```sql
CREATE TABLE stores (
  id BIGSERIAL PRIMARY KEY,
  shopify_domain VARCHAR NOT NULL UNIQUE,
  access_token TEXT NOT NULL, -- encrypted
  scope TEXT,
  api_version VARCHAR,
  active BOOLEAN DEFAULT true,
  metadata JSONB,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
```

#### questions
```sql
CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  store_id BIGINT REFERENCES stores(id),
  question_text TEXT NOT NULL,
  answer TEXT,
  confidence VARCHAR,
  query_used TEXT,
  data_points INTEGER,
  status VARCHAR NOT NULL, -- pending, processing, completed, failed
  error_message TEXT,
  processing_time_ms INTEGER,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_questions_store_id ON questions(store_id);
CREATE INDEX idx_questions_status ON questions(status);
CREATE INDEX idx_questions_created_at ON questions(created_at DESC);
```

## Security Considerations

### Authentication
- Shopify OAuth 2.0 flow
- Access tokens encrypted at rest
- Token rotation support

### API Security
- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration
- Request logging for audit

### Query Safety
- Read-only ShopifyQL queries
- Query validation layer
- No direct database access
- Parameterized queries

## Scalability

### Horizontal Scaling
- Stateless Rails API (can run multiple instances)
- Stateless Python service (can run multiple instances)
- Redis for shared cache and sessions

### Performance Optimization
- Redis caching (5-minute TTL)
- Shopify API response caching
- Async processing for long-running queries
- Connection pooling

### Rate Limiting
- Shopify API: 2 requests/second
- Internal rate limiting per store
- Queue system for burst traffic

## Monitoring & Logging

### Metrics
- Request latency
- Cache hit rate
- Shopify API usage
- Error rates
- Agent processing time

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking
- Performance profiling

## Deployment Architecture

### Development
```
localhost:3000 - Rails API
localhost:8000 - Python Agent
localhost:6379 - Redis
localhost:5432 - PostgreSQL
```

### Production (Recommended)
```
Load Balancer
  ↓
Rails API (multiple instances)
  ↓
Python Agent (multiple instances)
  ↓
Redis Cluster
PostgreSQL (primary + replica)
```

## Future Enhancements

1. **Conversation Memory**
   - Store conversation context
   - Support follow-up questions
   - Multi-turn dialogue

2. **Advanced Analytics**
   - Predictive modeling
   - Trend analysis
   - Anomaly detection

3. **Dashboard**
   - Visual analytics
   - Real-time metrics
   - Custom reports

4. **Multi-Store Support**
   - Aggregate analytics across stores
   - Comparative analysis
   - Consolidated reporting