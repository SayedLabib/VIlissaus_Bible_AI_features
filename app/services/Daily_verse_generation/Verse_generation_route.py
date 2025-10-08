from fastapi import APIRouter, HTTPException, Request, Response
import time
import logging
from app.services.Daily_verse_generation.Verse_generation_services import generate_random_verses
from app.services.Daily_verse_generation.Verse_generation_schema import VerseGenerationResponse

# Set up logging
logger = logging.getLogger(__name__)

verse_router = APIRouter(
    tags=["Daily_Verses"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}, 
        200: {"description": "Successfully generated verses and prayers"}
    }
)

@verse_router.get("/verses/random", response_model=VerseGenerationResponse)
async def get_random_verses(request: Request, response: Response):
    """
    Generate 15 random Bible verses with contextual meanings and 15 prayers.
    
    Returns:
        VerseGenerationResponse: A structured response containing 15 verses and 15 prayers
    """
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    
    logger.info(f"Verse generation requested by {client_ip}")
    
    try:
        # Generate verses and prayers using concurrent API calls
        result_dict = generate_random_verses()
        
        # Create the response model
        verse_response = VerseGenerationResponse(**result_dict)
        
        # Log success
        execution_time = time.time() - start_time
        logger.info(f"Verse generation completed in {execution_time:.2f}s")
        
        return verse_response
        
    except Exception as e:
        # Log the error with details
        logger.error(f"Failed to generate verses: {str(e)}", exc_info=True)
        
        # Return error to client
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate verses and prayers: {str(e)}"
        )
