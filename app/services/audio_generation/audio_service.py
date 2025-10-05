import requests
import uuid
import base64
from app.core.config import settings


class AudioGenerationService:
    
    def __init__(self):
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = "pNInz6obpgDQGcFmaJgB"
        
    def generate_audio(self, text: str, request_id: str = None) -> dict:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, stream=True)
            
            if response.status_code == 200:
                audio_content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        audio_content += chunk
                
                # Store in memory cache with request_id
                if not request_id:
                    request_id = str(uuid.uuid4())
                
                # Store temporarily (you can use Redis or similar for production)
                AudioGenerationService._audio_cache = getattr(AudioGenerationService, '_audio_cache', {})
                AudioGenerationService._audio_cache[request_id] = audio_content
                
                return {
                    "status": 200,
                    "success": True,
                    "request_id": request_id,
                    "audio_content": audio_content
                }
            else:
                return {
                    "status": response.status_code,
                    "success": False,
                    "request_id": None,
                    "audio_content": None
                }
                
        except Exception:
            return {
                "status": 500,
                "success": False,
                "request_id": None,
                "audio_content": None
            }
    
    @staticmethod
    def get_cached_audio(request_id: str):
        cache = getattr(AudioGenerationService, '_audio_cache', {})
        return cache.get(request_id)
