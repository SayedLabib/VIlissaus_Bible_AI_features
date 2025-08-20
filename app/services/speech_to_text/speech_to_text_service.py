import openai
from openai import AsyncOpenAI
import tempfile
import os
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.sync_client = openai.OpenAI(api_key=settings.openai_api_key)  # For transcription which doesn't have async support yet
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
                    response = self.sync_client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file
                    )
                return response.text
            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    async def get_bible_gpt_response(self, transcribed_text: str) -> str:
        """Generate Bible-related response using GPT-4 model"""
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
        try:
            # Prepare messages in the new chat format
            messages = [
                {"role": "system", "content": BIBLE_SYSTEM_PROMPT},
                {"role": "user", "content": transcribed_text}
            ]

            # Send the request to GPT-4 using the new chat completions API
            response = await self.client.chat.completions.create(
                model=settings.openai_model,  # Use the configured model
                messages=messages,
                max_tokens=512,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating Bible response: {e}")
            raise


# Create service instance
stt_service = STTService()