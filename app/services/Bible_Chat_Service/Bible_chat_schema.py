from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class BibleChatRequest(BaseModel):
    """Simple schema for Bible chat requests"""
    query: str = Field(
        ..., 
        min_length=2, 
        max_length=2000, 
        description="User's question or message about the Bible"
    )
    
    @validator('query')
    def validate_query_content(cls, v):
        """Validate query content"""
        if not v.strip():
            raise ValueError("Query cannot be empty or only whitespace")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What does the Bible say about forgiveness?"
            }
        }

class BibleChatResponse(BaseModel):
    """Simple schema for Bible chat responses"""
    success: bool = Field(..., description="Whether the request was successful")
    response: str = Field(..., description="The AI's response to the Bible query")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was generated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "The Bible teaches about forgiveness in many passages. Jesus taught us to pray 'forgive us our debts, as we also have forgiven our debtors' (Matthew 6:12, NIV). In Ephesians 4:32, Paul writes...",
                "timestamp": "2025-07-21T10:30:00"
            }
        }

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    response: str = Field(..., description="User-friendly error message")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "API key not configured",
                "response": "I apologize, but I'm unable to process your request at this time.",
                "timestamp": "2025-07-21T10:30:00"
            }
        }
