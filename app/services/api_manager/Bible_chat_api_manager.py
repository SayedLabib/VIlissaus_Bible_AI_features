from openai import AsyncOpenAI
from typing import Dict, Any
from app.core.config import settings, BIBLE_SYSTEM_PROMPT

class BibleChatAPIManager:
    """Manages OpenAI API interactions for Bible chat functionality"""
    
    def __init__(self):
        # Get configuration from settings
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.max_tokens = 1500
        self.temperature = 0.7
        self.top_p = 0.9
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0
        
        # Initialize the OpenAI client
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # System prompt for Bible-focused responses
        self.system_prompt = BIBLE_SYSTEM_PROMPT
    
    async def generate_bible_response(self, user_query: str) -> Dict[str, Any]:
        """
        Generate a Bible-focused response using OpenAI
        
        Args:
            user_query: The user's question or request about the Bible
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "usage": response.usage.model_dump() if response.usage else None,
                "model": self.model
            }
            
        except Exception as e:
            # Handle both OpenAI errors and general exceptions
            return {
                "success": False,
                "error": f"API error: {str(e)}",
                "response": "I apologize, but I'm experiencing difficulties connecting to the AI service. Please try again in a moment."
            }
