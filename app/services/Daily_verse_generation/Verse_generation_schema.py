from pydantic import BaseModel, Field
from typing import Dict


class VerseGenerationResponse(BaseModel):
    """Response model for verse generation"""
    verses: Dict[str, str] = Field(
        ..., 
        example={
            "verse01": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. - John 3:16",
            "verse02": "Trust in the Lord with all your heart and lean not on your own understanding. - Proverbs 3:5",
            "verse03": "I can do all this through him who gives me strength. - Philippians 4:13",
            "verse04": "The Lord is my shepherd; I shall not want. - Psalm 23:1",
            "verse05": "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go. - Joshua 1:9"
        },
        description="Dictionary of Bible verses with proper biblical references, keys verse01 to verse15"
    )