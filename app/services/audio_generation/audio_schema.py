from pydantic import BaseModel, Field


class AudioGenerationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class AudioGenerationResponse(BaseModel):
    status: int
    success: bool
    audio_url: str
