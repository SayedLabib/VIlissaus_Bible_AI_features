from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import configuration
from app.core.config import settings, CORS_CONFIG

# Import routers
from app.services.Bible_Chat_Service.Bible_chat_route import bible_chat_router

from app.services.Daily_verse_generation.Verse_generation_route import verse_router as verse_generation_router

from app.services.speech_to_text.speech_to_text_route import router as stt_router



# Create FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",  # Always enable docs
    redoc_url="/redoc"  # Always enable redoc
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

# Include routers
app.include_router(bible_chat_router, prefix=settings.api_v1_prefix)
app.include_router(verse_generation_router, prefix=settings.api_v1_prefix)
app.include_router(stt_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "description": settings.app_description,
        "environment": settings.environment,
        "endpoints": {
            "bible_chat": f"{settings.api_v1_prefix}/bible-chat/query",
            "verse_generation": f"{settings.api_v1_prefix}/verse-generation/random",
            "speech_to_text": f"{settings.api_v1_prefix}/stt/transcribe",
            "stt_info": f"{settings.api_v1_prefix}/stt/info",
            "health_check": f"{settings.api_v1_prefix}/bible-chat/health",
            "examples": f"{settings.api_v1_prefix}/bible-chat/examples",
            "documentation": "/docs"
        },
        "usage": {
            "endpoint": f"POST {settings.api_v1_prefix}/bible-chat/query",
            "payload": {"query": "Your Bible question here"},
            "example": {"query": "What does the Bible say about love?"}
        },
        "supported_bible_versions": settings.bible_versions
    }

@app.get("/health")
async def health_check():
    """General health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "bible_chat": "available",
        "openai_model": settings.openai_model,
        "supported_versions": settings.bible_versions
    }

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested resource was not found",
            "available_endpoints": [
                f"POST {settings.api_v1_prefix}/bible-chat/query",
                f"GET {settings.api_v1_prefix}/bible-chat/health",
                f"GET {settings.api_v1_prefix}/bible-chat/examples",
                f"POST {settings.api_v1_prefix}/verse-generation/random",
                f"POST {settings.api_v1_prefix}/stt/transcribe",
                f"GET {settings.api_v1_prefix}/stt/info",
                "GET /docs"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
