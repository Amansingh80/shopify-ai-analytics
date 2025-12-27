# Agent Flow Description

## Overview

The Shopify Analytics Agent implements an intelligent, multi-step workflow that transforms natural language questions into actionable business insights. This document details each step of the agent's reasoning process.

## Agent Workflow

### Phase 1: Intent Understanding

**Goal:** Extract structured information from unstructured natural language

**Process:**
1. Receive natural language question
2. Use LLM to analyze and classify:
   - **Domain identification:** Which data source? (orders, products, inventory, customers)
   - **Metric extraction:** What to measure? (count, sum, average, trend)
   - **Time period:** When? (last week, next month, specific dates)
   - **Filters:** Any conditions? (product name, status, price range)
   - **Intent summary:** High-level understanding

**Example:**
```
Input: "How many units of Product X will I need next month?"

Output:
{
  "domain": "orders",
  "metrics": ["sum", "average"],
  "time_period": "last_30_days",
  "filters": {"product_name": "Product X"},
  "intent_summary": "Forecast inventory needs based on historical sales"
}
```

**Reasoning:**
- Domain is "orders" because we need sales history
- Metrics include "sum" (total units) and "average" (daily rate)
- Time period is "last_30_days" to calculate trend
- Filter on specific product name
- Intent is forecasting, not just reporting

### Phase 2: Query Planning

**Goal:** Determine optimal data retrieval strategy

**Process:**
1. Analyze intent object
2. Decide which Shopify tables/endpoints to query
3. Identify required fields
4. Plan aggregations and joins
5. Consider data availability and API limits

**Example:**
```
Intent: Forecast inventory for Product X

Plan:
- Query: orders table
- Fields: product_id, quantity, created_at
- Filter: product_name = "Product X" AND created_at >= 30 days ago
- Aggregation: SUM(quantity), COUNT(DISTINCT order_id)
- Calculation: average_daily_sales = total_quantity / 30
- Forecast: average_daily_sales * 30 (for next month)
```

**Decision Factors:**
- Data freshness requirements
- Query complexity vs. accuracy trade-off
- API rate limits
- Cache availability

### Phase 3: ShopifyQL Generation

**Goal:** Create syntactically correct, optimized query

**Process:**
1. Use LLM with ShopifyQL expertise
2. Generate query based on plan
3. Apply query templates for common patterns
4. Optimize for performance

**Example:**
```sql
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
  AND product_name = 'Product X'
GROUP BY product_id
SELECT 
  product_id,
  product_name,
  SUM(quantity) as total_quantity,
  COUNT(DISTINCT order_id) as order_count
```

**Validation Checks:**
- Syntax correctness
- Read-only operations (no INSERT, UPDATE, DELETE)
- Valid table references
- Proper date formatting
- Reasonable LIMIT clauses

### Phase 4: Query Execution

**Goal:** Retrieve data efficiently and reliably

**Process:**
1. Check cache for recent results
2. If cache miss:
   - Execute query against Shopify API
   - Handle rate limiting
   - Retry on transient failures
3. Validate response data
4. Cache results (5-minute TTL)

**Error Handling:**
- **Empty results:** Return explanation, not error
- **API errors:** Retry with exponential backoff
- **Timeout:** Simplify query or use cached data
- **Invalid query:** Regenerate with corrections

**Example Response:**
```json
{
  "orders": [
    {
      "product_id": 12345,
      "product_name": "Product X",
      "total_quantity": 300,
      "order_count": 45
    }
  ]
}
```

### Phase 5: Data Processing

**Goal:** Transform raw data into meaningful metrics

**Process:**
1. Parse API response
2. Apply business logic:
   - Calculate averages
   - Identify trends
   - Detect anomalies
   - Project future values
3. Assess data quality and confidence

**Example Calculation:**
```python
total_quantity = 300 units
days = 30
average_daily_sales = 300 / 30 = 10 units/day

# Forecast for next month (30 days)
forecasted_need = 10 * 30 = 300 units

# Add safety buffer (20%)
recommended_reorder = 300 * 1.2 = 360 units

confidence = "medium" # based on data consistency
```

### Phase 6: Result Explanation

**Goal:** Convert technical metrics to business insights

**Process:**
1. Use LLM to generate explanation
2. Include:
   - Clear answer with specific numbers
   - Reasoning and methodology
   - Actionable recommendations
   - Confidence level
   - Caveats or assumptions

**Example Output:**
```json
{
  "answer": "Based on the last 30 days, you sell around 10 units of Product X per day. For next month, you should reorder at least 300 units. I recommend ordering 360 units (20% buffer) to avoid stockouts.",
  "confidence": "medium",
  "reasoning": "Calculated from 300 units sold over 30 days across 45 orders. Sales appear consistent. Added 20% safety buffer for demand variability.",
  "data_points": 45
}
```

**Language Guidelines:**
- Avoid technical jargon
- Use concrete numbers
- Provide context
- Offer recommendations
- Be honest about uncertainty

## Advanced Agent Capabilities

### Handling Ambiguity

**Scenario:** Vague or incomplete questions

**Strategy:**
1. Make reasonable assumptions
2. State assumptions in response
3. Offer to refine with more details

**Example:**
```
Question: "What are my best products?"

Agent reasoning:
- "Best" could mean: highest revenue, most units sold, highest margin
- Time period not specified
- Assume: highest revenue, last 30 days
- State assumption in answer
```

### Multi-Step Reasoning

**Scenario:** Complex questions requiring multiple queries

**Strategy:**
1. Break down into sub-questions
2. Execute queries sequentially
3. Combine results
4. Synthesize final answer

**Example:**
```
Question: "Which products are likely to go out of stock in 7 days?"

Steps:
1. Get current inventory levels
2. Get sales velocity (last 14 days)
3. Calculate days until stockout
4. Filter products with < 7 days remaining
5. Rank by urgency
```

### Error Recovery

**Scenario:** Query fails or returns unexpected results

**Strategy:**
1. Analyze failure reason
2. Attempt alternative approach:
   - Simplify query
   - Use different data source
   - Adjust time period
3. If all fail, explain limitation clearly

## Performance Optimization

### Caching Strategy
- Cache query results (5 minutes)
- Cache intent classifications (1 hour)
- Cache store metadata (24 hours)

### Query Optimization
- Use LIMIT to restrict result size
- Aggregate data server-side when possible
- Avoid unnecessary JOINs
- Use indexed fields in WHERE clauses

### Parallel Processing
- Execute independent queries concurrently
- Batch similar requests
- Pre-fetch common data

## Confidence Scoring

The agent assigns confidence levels based on:

**High Confidence:**
- Large dataset (100+ data points)
- Recent data (< 7 days old)
- Consistent patterns
- Simple, direct query

**Medium Confidence:**
- Moderate dataset (20-100 data points)
- Data up to 30 days old
- Some variability
- Requires assumptions

**Low Confidence:**
- Small dataset (< 20 data points)
- Old data (> 30 days)
- High variability
- Complex extrapolation

## Future Enhancements

1. **Learning from Feedback**
   - Track answer accuracy
   - Improve prompts based on corrections
   - Personalize to store patterns

2. **Proactive Insights**
   - Detect anomalies automatically
   - Send alerts for important trends
   - Suggest questions to ask

3. **Multi-Turn Conversations**
   - Remember context
   - Handle follow-up questions
   - Clarify ambiguities interactively