# API Examples

## Authentication

### 1. Initiate Shopify OAuth

**Request:**
```bash
GET /api/v1/auth/shopify?shop=example-store.myshopify.com
```

**Response:**
```json
{
  "auth_url": "https://example-store.myshopify.com/admin/oauth/authorize?client_id=...&scope=read_orders,read_products&redirect_uri=..."
}
```

### 2. OAuth Callback (handled automatically)

**Request:**
```bash
GET /api/v1/auth/shopify/callback?code=...&shop=example-store.myshopify.com
```

**Response:**
```json
{
  "message": "Authentication successful",
  "store": {
    "id": 1,
    "domain": "example-store.myshopify.com"
  }
}
```

## Analytics Questions

### Example 1: Inventory Forecasting

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "How many units of Product X will I need next month?"
}
```

**Response:**
```json
{
  "data": {
    "id": "123",
    "type": "question",
    "attributes": {
      "question_text": "How many units of Product X will I need next month?",
      "answer": "Based on the last 30 days, you sell around 10 units of Product X per day. For next month, you should reorder at least 300 units. I recommend ordering 360 units (20% buffer) to avoid stockouts.",
      "confidence": "medium",
      "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) AND product_name = 'Product X' GROUP BY product_id",
      "data_points": 45,
      "status": "completed",
      "processing_time_ms": 2340,
      "created_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Example 2: Stock Alert

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "Which products are likely to go out of stock in 7 days?"
}
```

**Response:**
```json
{
  "data": {
    "id": "124",
    "type": "question",
    "attributes": {
      "question_text": "Which products are likely to go out of stock in 7 days?",
      "answer": "Based on current inventory and sales velocity, 3 products need immediate attention:\n\n1. **Blue T-Shirt (SKU: BLU-001)**: 15 units left, selling 3/day → Out of stock in 5 days\n2. **Red Hoodie (SKU: RED-002)**: 20 units left, selling 3.5/day → Out of stock in 6 days\n3. **Black Cap (SKU: BLK-003)**: 18 units left, selling 2.8/day → Out of stock in 6 days\n\nRecommendation: Reorder these items immediately to avoid stockouts.",
      "confidence": "high",
      "query_used": "FROM inventory JOIN orders ON product_id WHERE created_at >= DATE_SUB(NOW(), INTERVAL 14 DAY)",
      "data_points": 127,
      "status": "completed",
      "processing_time_ms": 3120,
      "created_at": "2024-01-15T10:35:00Z"
    }
  }
}
```

### Example 3: Top Selling Products

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "What were my top 5 selling products last week?"
}
```

**Response:**
```json
{
  "data": {
    "id": "125",
    "type": "question",
    "attributes": {
      "question_text": "What were my top 5 selling products last week?",
      "answer": "Here are your top 5 best-sellers from last week:\n\n1. **Wireless Earbuds** - 87 units sold, $4,350 revenue\n2. **Phone Case Pro** - 65 units sold, $1,950 revenue\n3. **USB-C Cable** - 54 units sold, $810 revenue\n4. **Screen Protector** - 48 units sold, $720 revenue\n5. **Charging Dock** - 42 units sold, $1,680 revenue\n\nTotal: 296 units, $9,510 revenue from these top products.",
      "confidence": "high",
      "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) GROUP BY product_id ORDER BY SUM(quantity) DESC LIMIT 5",
      "data_points": 296,
      "status": "completed",
      "processing_time_ms": 1890,
      "created_at": "2024-01-15T10:40:00Z"
    }
  }
}
```

### Example 4: Reorder Calculation

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "How much inventory should I reorder based on last 30 days sales?"
}
```

**Response:**
```json
{
  "data": {
    "id": "126",
    "type": "question",
    "attributes": {
      "question_text": "How much inventory should I reorder based on last 30 days sales?",
      "answer": "Based on your sales over the last 30 days, here's my reorder recommendation:\n\n**Total Units Sold:** 1,245 units across all products\n**Average Daily Sales:** 41.5 units/day\n**Current Inventory:** 380 units\n**Days of Stock Remaining:** ~9 days\n\n**Recommended Reorder Quantities:**\n- For 30-day coverage: 1,245 units\n- With 20% safety buffer: 1,494 units\n- Net reorder needed: 1,114 units (after current inventory)\n\nPriority items to reorder immediately:\n1. Wireless Earbuds: 250 units\n2. Phone Case Pro: 180 units\n3. USB-C Cable: 150 units\n\nThis ensures you won't run out of stock for the next month.",
      "confidence": "high",
      "query_used": "FROM orders WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) GROUP BY product_id",
      "data_points": 1245,
      "status": "completed",
      "processing_time_ms": 2670,
      "created_at": "2024-01-15T10:45:00Z"
    }
  }
}
```

### Example 5: Repeat Customers

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "Which customers placed repeat orders in the last 90 days?"
}
```

**Response:**
```json
{
  "data": {
    "id": "127",
    "type": "question",
    "attributes": {
      "question_text": "Which customers placed repeat orders in the last 90 days?",
      "answer": "You have 23 repeat customers in the last 90 days! Here are your top 5 most loyal customers:\n\n1. **Sarah Johnson** (sarah.j@email.com)\n   - 7 orders, $1,240 total spent\n   - Last order: 3 days ago\n\n2. **Michael Chen** (m.chen@email.com)\n   - 6 orders, $980 total spent\n   - Last order: 1 week ago\n\n3. **Emily Rodriguez** (emily.r@email.com)\n   - 5 orders, $875 total spent\n   - Last order: 5 days ago\n\n4. **David Kim** (d.kim@email.com)\n   - 5 orders, $820 total spent\n   - Last order: 2 weeks ago\n\n5. **Lisa Anderson** (lisa.a@email.com)\n   - 4 orders, $690 total spent\n   - Last order: 1 week ago\n\n**Insight:** These 23 repeat customers represent 18% of your total revenue. Consider a loyalty program!",
      "confidence": "high",
      "query_used": "FROM customers WHERE orders_count > 1 AND last_order_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)",
      "data_points": 23,
      "status": "completed",
      "processing_time_ms": 2100,
      "created_at": "2024-01-15T10:50:00Z"
    }
  }
}
```

## Error Responses

### Invalid Store

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "nonexistent-store.myshopify.com",
  "question": "What are my sales?"
}
```

**Response:**
```json
{
  "error": "Store not found or inactive"
}
```
**Status Code:** 404

### Processing Error

**Request:**
```bash
POST /api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "Show me data for product that doesn't exist"
}
```

**Response:**
```json
{
  "data": {
    "id": "128",
    "type": "question",
    "attributes": {
      "question_text": "Show me data for product that doesn't exist",
      "answer": "I couldn't find any data for that product. This could mean:\n1. The product name doesn't match exactly\n2. The product has no sales history\n3. The product was recently added\n\nTry asking about a specific product by its exact name, or ask 'What products do I have?' to see your catalog.",
      "confidence": "low",
      "query_used": "FROM products WHERE name LIKE '%doesn't exist%'",
      "data_points": 0,
      "status": "completed",
      "processing_time_ms": 1450,
      "created_at": "2024-01-15T10:55:00Z"
    }
  }
}
```

## Retrieving Question History

**Request:**
```bash
GET /api/v1/questions?store_id=example-store.myshopify.com&page=1&per_page=10
```

**Response:**
```json
{
  "data": [
    {
      "id": "127",
      "type": "question",
      "attributes": {
        "question_text": "Which customers placed repeat orders in the last 90 days?",
        "answer": "You have 23 repeat customers...",
        "confidence": "high",
        "status": "completed",
        "created_at": "2024-01-15T10:50:00Z"
      }
    },
    {
      "id": "126",
      "type": "question",
      "attributes": {
        "question_text": "How much inventory should I reorder?",
        "answer": "Based on your sales...",
        "confidence": "high",
        "status": "completed",
        "created_at": "2024-01-15T10:45:00Z"
      }
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 3,
    "total_count": 27
  }
}
```

## cURL Examples

### Ask a Question
```bash
curl -X POST http://localhost:3000/api/v1/questions \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "example-store.myshopify.com",
    "question": "What were my top selling products last week?"
  }'
```

### Get Question Details
```bash
curl -X GET http://localhost:3000/api/v1/questions/123
```

### List Questions
```bash
curl -X GET "http://localhost:3000/api/v1/questions?store_id=example-store.myshopify.com&page=1"
```

## Python Client Example

```python
import requests

class ShopifyAnalyticsClient:
    def __init__(self, base_url, store_id):
        self.base_url = base_url
        self.store_id = store_id
    
    def ask_question(self, question):
        response = requests.post(
            f"{self.base_url}/api/v1/questions",
            json={
                "store_id": self.store_id,
                "question": question
            }
        )
        return response.json()
    
    def get_question(self, question_id):
        response = requests.get(
            f"{self.base_url}/api/v1/questions/{question_id}"
        )
        return response.json()

# Usage
client = ShopifyAnalyticsClient(
    base_url="http://localhost:3000",
    store_id="example-store.myshopify.com"
)

result = client.ask_question("What are my top products?")
print(result["data"]["attributes"]["answer"])
```