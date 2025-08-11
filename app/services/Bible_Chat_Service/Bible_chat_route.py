from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from .Bible_chat_schema import BibleChatRequest, BibleChatResponse, ErrorResponse
from .Bible_chat_service import BibleChatService

# Create router instance
bible_chat_router = APIRouter(
    prefix="/bible-chat",
    tags=["Bible Chat"],
    responses={404: {"description": "Not found"}}
)

# Dependency to get service instance
def get_bible_chat_service() -> BibleChatService:
    return BibleChatService()

@bible_chat_router.post(
    "/query",
    response_model=BibleChatResponse,
    summary="AI Bible Chat",
    description="Ask any question about the Bible and get AI-powered responses with scripture references"
)
async def bible_chat_query(
    request: BibleChatRequest,
    service: BibleChatService = Depends(get_bible_chat_service)
) -> Dict[str, Any]:
    """
    Main Bible chat endpoint for asking questions and getting biblical guidance.
    
    The AI will:
    - Answer questions based on KJV, NIV, ESV, NLT Bible versions
    - Generate prayers when requested
    - Acknowledge contradictions or different interpretations
    - Provide relevant scripture references
    - Maintain a respectful, spiritual tone
    
    **Supported Bible Versions:** KJV, NIV, ESV, NLT
    
    **Query Limits:** 
    - Minimum length: 2 characters
    - Maximum length: 2000 characters
    """
    try:
        # Validate the query
        is_valid, error_message = service.validate_query(request.query)
        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"Validation error: {error_message}",
                    "response": "Please provide a valid Bible-related question.",
                    "timestamp": ""
                }
            )
        
        # Process the Bible query
        response = await service.process_bible_query(request)
        
        if response["success"]:
            return JSONResponse(
                status_code=200,
                content=response
            )
        else:
            return JSONResponse(
                status_code=500,
                content=response
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Internal server error: {str(e)}",
                "response": "I apologize, but I'm unable to process your Bible question at the moment. Please try again later.",
                "timestamp": ""
            }
        )

@bible_chat_router.get(
    "/health",
    summary="Health Check",
    description="Check if the Bible chat service is running properly"
)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the Bible chat service
    """
    try:
        # Test service initialization
        service = BibleChatService()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "service": "Bible Chat Service",
                "status": "healthy",
                "message": "Service is running properly",
                "endpoint": "/api/v1/bible-chat/query",
                "supported_versions": ["KJV", "NIV", "ESV", "NLT"],
                "query_limits": {
                    "min_length": 2,
                    "max_length": 2000
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "service": "Bible Chat Service",
                "status": "unhealthy",
                "error": str(e),
                "message": "Service configuration error"
            }
        )

@bible_chat_router.get(
    "/examples",
    summary="Example Queries",
    description="Get example queries you can ask the Bible chat AI"
)
async def get_examples() -> Dict[str, Any]:
    """
    Get example queries for the Bible chat service
    """
    examples = {
        "bible_questions": [
            "What does the Bible say about love?",
            "How many books are in the Bible?",
            "Who wrote the book of Romans?",
            "What is the Gospel?",
            "What does the Bible teach about forgiveness?"
        ],
        "prayer_requests": [
            "Can you generate a prayer for healing?",
            "Write a prayer of thanksgiving",
            "Create a prayer for wisdom and guidance",
            "Generate a prayer for peace",
            "Write a prayer for strength during difficult times"
        ],
        "version_comparisons": [
            "Compare John 3:16 in KJV, NIV, ESV, and NLT",
            "Show me Psalm 23 in different translations",
            "Compare the wording of the Lord's Prayer in different versions"
        ],
        "theological_questions": [
            "What are the different Christian views on baptism?",
            "Are there contradictions in the Bible?",
            "What does the Bible say about predestination?",
            "Explain the Trinity from a biblical perspective"
        ]
    }
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Example queries for Bible Chat AI",
            "examples": examples,
            "supported_versions": ["KJV", "NIV", "ESV", "NLT"],
            "usage": "Send a POST request to /api/v1/bible-chat/query with your question in the 'query' field",
            "query_limits": {
                "min_length": 2,
                "max_length": 2000
            }
        }
    )
