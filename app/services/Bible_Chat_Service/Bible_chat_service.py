from typing import Dict, Any
from datetime import datetime

from app.services.api_manager.Bible_chat_api_manager import BibleChatAPIManager
from .Bible_chat_schema import BibleChatRequest, BibleChatResponse

class BibleChatService:
    """Service class for handling Bible chat functionality"""
    
    def __init__(self):
        self.api_manager = BibleChatAPIManager()
        self.min_query_length = 2
        self.max_query_length = 2000
    
    async def process_bible_query(self, request: BibleChatRequest) -> Dict[str, Any]:
        """
        Process a Bible query and return AI response
        
        Args:
            request: BibleChatRequest object with user query
            
        Returns:
            Dictionary with response data
        """
        try:
            # Generate response using API manager
            api_response = await self.api_manager.generate_bible_response(request.query)
            
            if api_response["success"]:
                return {
                    "success": True,
                    "response": api_response["response"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": api_response["error"],
                    "response": api_response["response"],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Service error: {str(e)}",
                "response": "I apologize, but I encountered an error processing your Bible question. Please try again.",
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        Validate the user query
        
        Args:
            query: User's query string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "Query cannot be empty"
        
        if len(query.strip()) < self.min_query_length:
            return False, f"Query must be at least {self.min_query_length} characters long"
        
        if len(query) > self.max_query_length:
            return False, f"Query is too long. Maximum {self.max_query_length} characters allowed"
        
        return True, ""
