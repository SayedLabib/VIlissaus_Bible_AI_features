from fastapi import APIRouter, HTTPException
from app.services.Daily_verse_generation.Verse_generation_services import generate_random_verses
from app.services.Daily_verse_generation.Verse_generation_schema import VerseGenerationResponse

verse_router = APIRouter(
    tags=["Daily_Verses"],
    responses={404: {"description": "Not found"}}
)

@verse_router.get("/verses/random", response_model=VerseGenerationResponse)
async def get_random_verses():
    """Generate 15 random Bible verses with contextual meanings"""
    try:
        verses = generate_random_verses()
        return VerseGenerationResponse(**verses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate verses: {str(e)}")
