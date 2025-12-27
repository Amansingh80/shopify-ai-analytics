from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
from app.agents.shopify_agent import ShopifyAnalyticsAgent
from app.services.cache_service import CacheService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Shopify AI Analytics Agent",
    description="LLM-powered agent for Shopify analytics",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
cache_service = CacheService()

class AnalyzeRequest(BaseModel):
    store_id: str = Field(..., description="Shopify store domain")
    question: str = Field(..., description="Natural language question")
    context: Dict[str, Any] = Field(..., description="Store context and credentials")

class AnalyzeResponse(BaseModel):
    answer: str
    confidence: str
    query_used: Optional[str] = None
    data_points: int
    reasoning: Optional[str] = None

@app.get("/")
async def root():
    return {
        "service": "Shopify AI Analytics Agent",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_question(request: AnalyzeRequest):
    """
    Main endpoint for analyzing natural language questions about Shopify data.
    
    The agent will:
    1. Understand the user's intent
    2. Generate appropriate ShopifyQL query
    3. Execute the query
    4. Convert results to business-friendly language
    """
    try:
        logger.info(f"Processing question for store: {request.store_id}")
        logger.info(f"Question: {request.question}")
        
        # Initialize agent
        agent = ShopifyAnalyticsAgent(
            store_id=request.store_id,
            access_token=request.context.get("access_token"),
            api_version=request.context.get("api_version", "2024-01"),
            cache_service=cache_service
        )
        
        # Process question
        result = await agent.process_question(request.question)
        
        logger.info(f"Successfully processed question. Confidence: {result['confidence']}")
        
        return AnalyzeResponse(
            answer=result["answer"],
            confidence=result["confidence"],
            query_used=result.get("query_used"),
            data_points=result.get("data_points", 0),
            reasoning=result.get("reasoning")
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )

@app.post("/api/validate-query")
async def validate_query(query: str):
    """Validate ShopifyQL query syntax"""
    try:
        # Basic validation logic
        is_valid = ShopifyAnalyticsAgent.validate_shopifyql(query)
        return {"valid": is_valid, "query": query}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)