INTENT_CLASSIFICATION_PROMPT = """
You are an expert at understanding business questions about e-commerce data.

Analyze this question and extract:
1. Domain (orders, products, inventory, customers)
2. Metrics needed (count, sum, average, etc.)
3. Time period (if mentioned)
4. Any filters or conditions

Question: {question}

Return a JSON object with this structure:
{{
    "domain": "orders|products|inventory|customers",
    "metrics": ["count", "sum", "average"],
    "time_period": "last_7_days|last_30_days|last_week|next_month|etc",
    "filters": {{"product_name": "X", "status": "active"}},
    "intent_summary": "brief description"
}}

Be precise and only include information explicitly mentioned or clearly implied.
"""

QUERY_GENERATION_PROMPT = """
You are an expert at writing ShopifyQL queries.

Generate a ShopifyQL query to answer this question:
Question: {question}

Intent Analysis: {intent}
Domain: {domain}

ShopifyQL Guidelines:
- Use FROM clause with valid tables: orders, products, inventory, customers, line_items
- Use WHERE for filtering
- Use GROUP BY for aggregations
- Use ORDER BY for sorting
- Use LIMIT to restrict results
- Date format: 'YYYY-MM-DD'
- Use proper SQL syntax

Example queries:
1. "Top 5 products last week":
   FROM orders
   WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
   GROUP BY product_id
   ORDER BY SUM(quantity) DESC
   LIMIT 5

2. "Low inventory products":
   FROM inventory
   WHERE quantity < 10
   ORDER BY quantity ASC

Generate ONLY the ShopifyQL query, no explanations:
"""

RESULT_EXPLANATION_PROMPT = """
You are a business analyst explaining data insights to store owners.

Question: {question}
Query Used: {query}
Data Retrieved: {data}

Convert this technical data into a clear, actionable business insight.

Guidelines:
- Use simple, non-technical language
- Provide specific numbers and recommendations
- Be concise but informative
- Include confidence level (high/medium/low)
- Add reasoning if helpful

Return JSON:
{{
    "answer": "Clear business-friendly explanation with specific numbers and recommendations",
    "confidence": "high|medium|low",
    "reasoning": "Brief explanation of how you arrived at this answer"
}}

Focus on actionable insights the store owner can use.
"""