from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.speech_to_text.speech_to_text_service import stt_service

router = APIRouter(tags=["Speech-to-Text"], prefix="/stt")

@router.post("/bible_ai_chat")
async def transcribe_and_respond(audio_file: UploadFile = File(...)):
    """Transcribe audio file and send to GPT-4 for chatbot response"""
    if not audio_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read file content
        content = await audio_file.read()
        
        # Transcribe the audio to text
        transcribed_text = await stt_service.transcribe(content, audio_file.filename)
        
        # Send the transcribed text to GPT-4 for a Bible-focused chatbot response
        chatbot_response = await stt_service.get_bible_gpt_response(transcribed_text)
        
        return {
            "success": True,
            "transcription": transcribed_text,
            "chatbot_response": chatbot_response,
            "filename": audio_file.filename
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing audio or generating response")
