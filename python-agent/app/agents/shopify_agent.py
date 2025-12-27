import os
from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from app.services.shopify_service import ShopifyService
from app.services.cache_service import CacheService
from app.prompts.agent_prompts import (
    INTENT_CLASSIFICATION_PROMPT,
    QUERY_GENERATION_PROMPT,
    RESULT_EXPLANATION_PROMPT
)

logger = logging.getLogger(__name__)

class ShopifyAnalyticsAgent:
    """
    Agentic workflow for Shopify analytics:
    1. Understand intent
    2. Plan data requirements
    3. Generate ShopifyQL
    4. Execute & validate
    5. Explain results
    """
    
    def __init__(
        self,
        store_id: str,
        access_token: str,
        api_version: str = "2024-01",
        cache_service: Optional[CacheService] = None
    ):
        self.store_id = store_id
        self.shopify_service = ShopifyService(
            store_id=store_id,
            access_token=access_token,
            api_version=api_version
        )
        self.cache_service = cache_service
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    async def process_question(self, question: str) -> Dict[str, Any]:
        """Main processing pipeline"""
        try:
            # Step 1: Understand intent
            intent = await self._classify_intent(question)
            logger.info(f"Classified intent: {intent}")
            
            # Step 2: Generate ShopifyQL query
            query = await self._generate_query(question, intent)
            logger.info(f"Generated query: {query}")
            
            # Step 3: Execute query
            data = await self._execute_query(query, intent)
            logger.info(f"Retrieved {len(data) if isinstance(data, list) else 1} data points")
            
            # Step 4: Explain results
            explanation = await self._explain_results(question, data, query)
            
            return {
                "answer": explanation["answer"],
                "confidence": explanation["confidence"],
                "query_used": query,
                "data_points": len(data) if isinstance(data, list) else 1,
                "reasoning": explanation.get("reasoning")
            }
            
        except Exception as e:
            logger.error(f"Error in agent pipeline: {str(e)}")
            raise
    
    async def _classify_intent(self, question: str) -> Dict[str, Any]:
        """Classify user intent and extract key information"""
        prompt = PromptTemplate(
            template=INTENT_CLASSIFICATION_PROMPT,
            input_variables=["question"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(question=question)
        
        # Parse LLM response
        import json
        try:
            intent = json.loads(result)
        except json.JSONDecodeError:
            # Fallback parsing
            intent = {
                "domain": "orders",
                "metrics": ["count"],
                "time_period": "last_30_days",
                "filters": {}
            }
        
        return intent
    
    async def _generate_query(self, question: str, intent: Dict[str, Any]) -> str:
        """Generate ShopifyQL query based on intent"""
        prompt = PromptTemplate(
            template=QUERY_GENERATION_PROMPT,
            input_variables=["question", "intent", "domain"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        query = await chain.arun(
            question=question,
            intent=str(intent),
            domain=intent.get("domain", "orders")
        )
        
        # Clean and validate query
        query = query.strip().strip("```sql").strip("```").strip()
        
        if not self.validate_shopifyql(query):
            raise ValueError(f"Generated invalid ShopifyQL: {query}")
        
        return query
    
    async def _execute_query(self, query: str, intent: Dict[str, Any]) -> Any:
        """Execute query against Shopify API"""
        domain = intent.get("domain", "orders")
        
        # Check cache first
        if self.cache_service:
            cache_key = f"{self.store_id}:{domain}:{query}"
            cached_result = self.cache_service.get(cache_key)
            if cached_result:
                logger.info("Returning cached result")
                return cached_result
        
        # Execute based on domain
        if domain == "orders":
            data = await self.shopify_service.query_orders(query)
        elif domain == "products":
            data = await self.shopify_service.query_products(query)
        elif domain == "inventory":
            data = await self.shopify_service.query_inventory(query)
        elif domain == "customers":
            data = await self.shopify_service.query_customers(query)
        else:
            raise ValueError(f"Unknown domain: {domain}")
        
        # Cache result
        if self.cache_service:
            self.cache_service.set(cache_key, data, ttl=300)  # 5 minutes
        
        return data
    
    async def _explain_results(
        self,
        question: str,
        data: Any,
        query: str
    ) -> Dict[str, str]:
        """Convert technical results to business-friendly explanation"""
        prompt = PromptTemplate(
            template=RESULT_EXPLANATION_PROMPT,
            input_variables=["question", "data", "query"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        explanation = await chain.arun(
            question=question,
            data=str(data)[:2000],  # Limit data size
            query=query
        )
        
        # Parse explanation
        import json
        try:
            result = json.loads(explanation)
        except json.JSONDecodeError:
            result = {
                "answer": explanation,
                "confidence": "medium"
            }
        
        return result
    
    @staticmethod
    def validate_shopifyql(query: str) -> bool:
        """Basic ShopifyQL validation"""
        query_lower = query.lower()
        
        # Must contain FROM clause
        if "from" not in query_lower:
            return False
        
        # Check for valid tables
        valid_tables = ["orders", "products", "inventory", "customers", "line_items"]
        has_valid_table = any(table in query_lower for table in valid_tables)
        
        if not has_valid_table:
            return False
        
        # No dangerous operations
        dangerous = ["drop", "delete", "update", "insert", "alter"]
        if any(op in query_lower for op in dangerous):
            return False
        
        return True