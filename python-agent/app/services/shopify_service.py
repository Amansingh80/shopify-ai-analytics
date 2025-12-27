import requests
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ShopifyService:
    """Service for interacting with Shopify Admin API"""
    
    def __init__(self, store_id: str, access_token: str, api_version: str = "2024-01"):
        self.store_id = store_id
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://{store_id}/admin/api/{api_version}"
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Shopify API"""
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}.json"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Shopify API error: {str(e)}")
            raise
    
    async def query_orders(self, query: str) -> List[Dict[str, Any]]:
        """Query orders data"""
        # Parse query to extract filters
        filters = self._parse_query_filters(query)
        
        # Build API parameters
        params = {
            "status": "any",
            "limit": filters.get("limit", 50)
        }
        
        if filters.get("created_at_min"):
            params["created_at_min"] = filters["created_at_min"]
        
        if filters.get("created_at_max"):
            params["created_at_max"] = filters["created_at_max"]
        
        # Fetch orders
        result = self._make_request("orders", params)
        orders = result.get("orders", [])
        
        # Apply additional filtering and aggregation
        processed_data = self._process_orders(orders, query)
        
        return processed_data
    
    async def query_products(self, query: str) -> List[Dict[str, Any]]:
        """Query products data"""
        filters = self._parse_query_filters(query)
        
        params = {
            "limit": filters.get("limit", 50)
        }
        
        result = self._make_request("products", params)
        products = result.get("products", [])
        
        return self._process_products(products, query)
    
    async def query_inventory(self, query: str) -> List[Dict[str, Any]]:
        """Query inventory data"""
        filters = self._parse_query_filters(query)
        
        # Get inventory levels
        params = {"limit": filters.get("limit", 50)}
        
        result = self._make_request("inventory_levels", params)
        inventory = result.get("inventory_levels", [])
        
        return self._process_inventory(inventory, query)
    
    async def query_customers(self, query: str) -> List[Dict[str, Any]]:
        """Query customers data"""
        filters = self._parse_query_filters(query)
        
        params = {
            "limit": filters.get("limit", 50)
        }
        
        if filters.get("created_at_min"):
            params["created_at_min"] = filters["created_at_min"]
        
        result = self._make_request("customers", params)
        customers = result.get("customers", [])
        
        return self._process_customers(customers, query)
    
    def _parse_query_filters(self, query: str) -> Dict[str, Any]:
        """Extract filters from ShopifyQL-like query"""
        filters = {}
        query_lower = query.lower()
        
        # Extract LIMIT
        if "limit" in query_lower:
            try:
                limit_idx = query_lower.index("limit")
                limit_value = query[limit_idx:].split()[1]
                filters["limit"] = int(limit_value)
            except (ValueError, IndexError):
                pass
        
        # Extract date filters
        if "last" in query_lower and "day" in query_lower:
            if "7 day" in query_lower or "week" in query_lower:
                days = 7
            elif "30 day" in query_lower or "month" in query_lower:
                days = 30
            elif "90 day" in query_lower:
                days = 90
            else:
                days = 7
            
            filters["created_at_min"] = (
                datetime.now() - timedelta(days=days)
            ).isoformat()
        
        return filters
    
    def _process_orders(self, orders: List[Dict], query: str) -> List[Dict[str, Any]]:
        """Process and aggregate order data"""
        query_lower = query.lower()
        
        # Check if we need to group by product
        if "group by product" in query_lower or "by product" in query_lower:
            product_sales = {}
            
            for order in orders:
                for item in order.get("line_items", []):
                    product_id = item.get("product_id")
                    product_name = item.get("name")
                    quantity = item.get("quantity", 0)
                    
                    if product_id not in product_sales:
                        product_sales[product_id] = {
                            "product_id": product_id,
                            "product_name": product_name,
                            "total_quantity": 0,
                            "total_revenue": 0
                        }
                    
                    product_sales[product_id]["total_quantity"] += quantity
                    product_sales[product_id]["total_revenue"] += float(item.get("price", 0)) * quantity
            
            result = list(product_sales.values())
            
            # Sort by quantity if ORDER BY in query
            if "order by" in query_lower:
                result.sort(key=lambda x: x["total_quantity"], reverse=True)
            
            return result
        
        return orders
    
    def _process_products(self, products: List[Dict], query: str) -> List[Dict[str, Any]]:
        """Process product data"""
        return products
    
    def _process_inventory(self, inventory: List[Dict], query: str) -> List[Dict[str, Any]]:
        """Process inventory data"""
        query_lower = query.lower()
        
        # Filter low stock items
        if "where" in query_lower and "quantity" in query_lower:
            try:
                # Extract threshold
                threshold = 10  # default
                if "<" in query:
                    threshold_str = query.split("<")[1].split()[0]
                    threshold = int(threshold_str)
                
                inventory = [
                    item for item in inventory
                    if item.get("available", 0) < threshold
                ]
            except (ValueError, IndexError):
                pass
        
        return inventory
    
    def _process_customers(self, customers: List[Dict], query: str) -> List[Dict[str, Any]]:
        """Process customer data"""
        query_lower = query.lower()
        
        # Filter repeat customers
        if "repeat" in query_lower or "orders_count" in query_lower:
            customers = [
                c for c in customers
                if c.get("orders_count", 0) > 1
            ]
        
        return customers