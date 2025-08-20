import openai
import tempfile
import os
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = "whisper-1"
        self.supported_formats = {'mp3', 'mp4', 'wav', 'm4a', 'webm'}
        self.max_size_mb = 25

    async def transcribe(self, audio_data: bytes, filename: str) -> str:
        """Transcribe audio to text using OpenAI Whisper"""
        try:
            # Validate file size
            size_mb = len(audio_data) / (1024 * 1024)
            if size_mb > self.max_size_mb:
                raise ValueError(f"File too large: {size_mb:.1f}MB (max: {self.max_size_mb}MB)")

            # Validate format
            ext = filename.split('.')[-1].lower() if '.' in filename else ''
            if ext not in self.supported_formats:
                raise ValueError(f"Unsupported format: {ext}")

            # Create temp file and transcribe
            with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name

            try:
                with open(tmp_path, 'rb') as audio_file:
                    response = self.client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file
                    )
                return response.text
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

# Create service instance
stt_service = STTService()