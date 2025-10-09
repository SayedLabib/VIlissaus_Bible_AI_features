from pydantic import BaseModel, Field
from typing import Dict, Any, List


class VerseDetail(BaseModel):
    """Model for individual verse with text and context"""
    text: str = Field(
        ...,
        description="The complete Bible verse text",
        example="For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
    )
    context: str = Field(
        ...,
        description="The contextual meaning and explanation of what the verse actually means",
        example="This verse speaks about God's unconditional love for humanity and the sacrifice of Jesus Christ."
    )
    reference: str = Field(
        ...,
        description="The biblical reference for the verse",
        example="John 3:16"
    )


class PrayerDetail(BaseModel):
    """Model for individual prayer with title and full prayer text"""
    text: str = Field(
        ...,
        description="The title or name of the prayer",
        example="Morning Prayer for Guidance"
    )
    context: str = Field(
        ...,
        description="The complete prayer text",
        example="Heavenly Father, as I begin this new day, I come before You seeking Your wisdom and guidance. Please direct my steps and help me to make decisions that honor You. In Jesus' name, Amen."
    )


class VerseItem(BaseModel):
    verse_id: str
    details: VerseDetail


class PrayerItem(BaseModel):
    prayer_id: str
    details: PrayerDetail


class VerseGenerationResponse(BaseModel):
    """Response model for verse and prayer generation with verses and prayers in lists"""
    verses: List[VerseItem]
    prayers: List[PrayerItem]
