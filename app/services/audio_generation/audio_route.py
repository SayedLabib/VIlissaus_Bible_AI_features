from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.services.audio_generation.audio_schema import AudioGenerationRequest, AudioGenerationResponse
from app.services.audio_generation.audio_service import AudioGenerationService
import io

audio_router = APIRouter(prefix="/audio", tags=["Audio Generation"])

@audio_router.post("/generate", response_model=AudioGenerationResponse)
async def generate_audio(request: AudioGenerationRequest, http_request: Request):
    service = AudioGenerationService()
    result = service.generate_audio(request.text)
    
    if not result["success"]:
        raise HTTPException(status_code=result["status"], detail="Failed to generate audio")
    
    base_url = str(http_request.base_url).rstrip('/')
    audio_url = f"{base_url}/api/v1/audio/download/{result['request_id']}"
    
    return AudioGenerationResponse(
        status=result["status"],
        success=result["success"],
        audio_url=audio_url
    )


@audio_router.get("/download/{request_id}")
async def download_audio(request_id: str):
    audio_content = AudioGenerationService.get_cached_audio(request_id)
    
    if not audio_content:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    
    return StreamingResponse(
        io.BytesIO(audio_content),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename=preacher_{request_id}.mp3"}
    )
