from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.speech_to_text.speech_to_text_service import stt_service

router = APIRouter(tags=["Speech-to-Text"], prefix="/stt")

@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """Transcribe audio file to text"""
    if not audio_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read file content
        content = await audio_file.read()
        
        # Transcribe
        text = await stt_service.transcribe(content, audio_file.filename)
        
        return {
            "success": True,
            "text": text,
            "filename": audio_file.filename
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Transcription failed")

@router.get("/info")
async def get_info():
    """Get STT service information"""
    return {
        "model": "whisper-1",
        "supported_formats": ["mp3", "mp4", "wav", "m4a", "webm"],
        "max_size_mb": 25
    }
