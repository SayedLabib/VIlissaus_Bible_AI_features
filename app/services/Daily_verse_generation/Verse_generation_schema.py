from pydantic import BaseModel, Field
from typing import Dict


class VerseDetail(BaseModel):
    """Model for individual verse with text and context"""
    text: str = Field(
        ...,
        description="The complete Bible verse text with biblical reference",
        example="For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
    )
    context: str = Field(
        ...,
        description="The contextual meaning and explanation of what the verse actually means",
        example="This verse speaks about God's unconditional love for humanity and the sacrifice of Jesus Christ. It emphasizes that salvation and eternal life come through faith in Jesus, highlighting the core message of Christianity about God's redemptive love."
    )
    reference: str = Field(
        ...,
        description="The biblical reference for the verse",
        example="John 3:16"
    )


class VerseGenerationResponse(BaseModel):
    """Response model for verse generation with 15 verses"""
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