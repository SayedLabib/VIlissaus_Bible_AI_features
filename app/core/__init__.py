"""
Core module for Vilisasu Bible AI
Contains configuration and shared utilities
"""

from .config import settings, OPENAI_CONFIG, CORS_CONFIG, BIBLE_SYSTEM_PROMPT

__all__ = [
    "settings",
    "OPENAI_CONFIG", 
    "CORS_CONFIG",
    "BIBLE_SYSTEM_PROMPT"
]
