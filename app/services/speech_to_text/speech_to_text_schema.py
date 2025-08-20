from pydantic import BaseModel, Field
from typing import Optional

class SpeechToTextRequest(BaseModel):
    audio_file: bytes = Field(..., description="The audio file to transcribe")
    language: str = Field(..., description="The language of the audio")

class SpeechToTextResponse(BaseModel):
    transcription: str = Field(..., description="The transcribed text")