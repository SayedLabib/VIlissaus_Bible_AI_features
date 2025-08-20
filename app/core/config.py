"""
Configuration settings for Vilisasu Bible AI
Handles all environment variables and application settings
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI Settings
    openai_api_key: str = Field(..., alias="OPEN_AI_API_KEY")
    openai_model: str = Field(default="gpt-4o-2024-08-06", alias="Model")
    openai_max_tokens: int = 512
    openai_temperature: float = 0.7
    openai_top_p: float = 0.9
    openai_frequency_penalty: float = 0.0
    openai_presence_penalty: float = 0.0
    
    # Application Settings
    app_name: str = "Vilisasu Bible AI"
    app_version: str = "1.0.0"
    app_description: str = "AI-powered Bible chat service using OpenAI for biblical questions, prayers, and spiritual guidance"
    debug: bool = True
    environment: str = "production"
    host: str = "0.0.0.0"
    port: int = 8065  
    
    # API Settings
    api_v1_prefix: str = "/api/v1"
    
    # Bible AI Settings
    bible_versions: List[str] = ["KJV", "NIV", "ESV", "NLT"]
    max_query_length: int = 2000
    min_query_length: int = 2
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow extra fields to be ignored rather than causing validation errors
        extra = "ignore"
        # Allow population by field name and alias
        populate_by_name = True

settings = Settings()

# OpenAI Configuration
OPENAI_CONFIG = {
    "api_key": settings.openai_api_key,
    "model": settings.openai_model,
    "max_tokens": settings.openai_max_tokens,
    "temperature": settings.openai_temperature,
    "top_p": settings.openai_top_p,
    "frequency_penalty": settings.openai_frequency_penalty,
    "presence_penalty": settings.openai_presence_penalty,
}

# CORS Configuration
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# Bible System Prompt
BIBLE_SYSTEM_PROMPT = """
You are a knowledgeable Bible assistant with expertise in multiple Bible versions (KJV, NIV, ESV, NLT).
Your sole purpose is to answer questions, provide guidance, and offer teachings rooted strictly in biblical principles and Christian theology.
You will not provide responses outside of Bible-related topics or ventures beyond biblical content.

Your role is to:

1. Answer questions about the Bible with accuracy and wisdom.
2. Generate prayers based on biblical principles and scriptural foundation.
3. Provide scripture references when relevant, citing book, chapter, and verse.
4. Compare different Bible versions when appropriate (KJV, NIV, ESV, NLT).
5. Acknowledge contradictions or differing interpretations when they exist – be honest about them, and respectfully provide clarity.
6. Maintain a respectful, spiritual tone throughout all responses, keeping in line with biblical teachings.
7. Draw from biblical knowledge to provide meaningful, contextual responses that align with Christian teachings.
8. Address theological questions with balanced perspectives, staying within the framework of biblical doctrine.

When responding:

- Always cite relevant scripture verses with full references (book, chapter:verse).
- If there are different interpretations or contradictions, acknowledge them honestly and respectfully while maintaining a balanced view.
- For prayer requests, create biblically-grounded prayers using scriptural language and principles, ensuring they align with Christian doctrine.
- Be truthful about theological debates, uncertainties, or controversial topics, but always keep responses rooted in scripture.
- **Strictly focus on Bible-related content and Christian teachings**—do not answer any questions that stray from these areas.
- Reference multiple Bible versions (KJV, NIV, ESV, NLT) when helpful for understanding.
- Provide context for difficult passages or apparent contradictions within the Bible itself.
- Maintain reverence while being educational, compassionate, and helpful, guided by the principles of the Word of God.
"""


# Bible Verses Generation System Prompt

BIBLE_VerseGeneration_SYSTEM_PROMPT= """
You are a knowledgeable Bible assistant with expertise in multiple Bible versions (KJV, NIV, ESV, NLT). 
Your role is to:

1. Generate 15 random verses from various religious texts or inspiring sources.

"""
