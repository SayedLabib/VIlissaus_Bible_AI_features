from pydantic import BaseModel, Field
from typing import Dict, Any


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


class VerseGenerationResponse(BaseModel):
    """Response model for verse and prayer generation"""
    verse01: VerseDetail
    verse02: VerseDetail
    verse03: VerseDetail
    verse04: VerseDetail
    verse05: VerseDetail
    verse06: VerseDetail
    verse07: VerseDetail
    verse08: VerseDetail
    verse09: VerseDetail
    verse10: VerseDetail
    verse11: VerseDetail
    verse12: VerseDetail
    verse13: VerseDetail
    verse14: VerseDetail
    verse15: VerseDetail
    prayer01: PrayerDetail
    prayer02: PrayerDetail
    prayer03: PrayerDetail
    prayer04: PrayerDetail
    prayer05: PrayerDetail
    prayer06: PrayerDetail
    prayer07: PrayerDetail
    prayer08: PrayerDetail
    prayer09: PrayerDetail
    prayer10: PrayerDetail
    prayer11: PrayerDetail
    prayer12: PrayerDetail
    prayer13: PrayerDetail
    prayer14: PrayerDetail
    prayer15: PrayerDetail
