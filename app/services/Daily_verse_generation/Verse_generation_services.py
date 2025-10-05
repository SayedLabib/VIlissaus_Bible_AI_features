import openai
import json
import random
import time
from typing import Dict
from app.core.config import settings
from app.services.Daily_verse_generation.Verse_generation_schema import VerseDetail

client = openai.OpenAI(api_key=settings.openai_api_key)

def generate_random_verses() -> Dict[str, VerseDetail]:
    # Use timestamp and random seed for better variation
    random_seed = int(time.time() * 1000) + random.randint(1, 10000)
    bible_versions = ["KJV", "NIV", "ESV", "NLT"]
    
    # Randomly select which versions to prioritize for this generation
    primary_versions = random.sample(bible_versions, k=2)
    
    prompt = f"""Generate exactly 15 UNIQUE and DIVERSE Bible verses that are DIFFERENT from commonly used verses.

IMPORTANT: Use a mix of Bible versions (KJV, NIV, ESV, NLT). Prioritize {primary_versions[0]} and {primary_versions[1]} for this generation.

Return a JSON object with this EXACT structure:
{{
  "verses": [
    {{
      "text": "verse text without reference",
      "context": "detailed explanation",
      "reference": "Book Chapter:Verse"
    }}
  ]
}}

DIVERSITY REQUIREMENTS:
- DO NOT use famous verses like John 3:16, Psalm 23:1, Philippians 4:13
- Include verses from LESSER-KNOWN books: Habakkuk, Zephaniah, Malachi, Haggai, Obadiah, Philemon, Jude, 2 Peter, 3 John
- Mix Old Testament (60%) and New Testament (40%)
- Include different verse types: wisdom, prophecy, history, poetry, commands, promises
- Use random chapter numbers (not just chapter 1)
- Vary the Bible version for each verse (mention version in reference)
- Each verse must be COMPLETELY DIFFERENT from previous generations

VERSE CATEGORIES (mix these):
- Wisdom literature (Proverbs, Ecclesiastes, Job)
- Prophetic books (Isaiah, Jeremiah, Ezekiel, Minor Prophets)
- Epistles (Romans, Corinthians, Galatians, Ephesians, etc.)
- Historical narratives (Kings, Chronicles, Acts)
- Psalms (but NOT Psalm 23, 91, or 103)
- Gospel teachings (but avoid the most famous passages)

Random seed: {random_seed}

Return ONLY valid JSON, no other text."""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are a biblical scholar with deep knowledge of the entire Bible. Generate DIVERSE and UNIQUE verses from all 66 books. Avoid commonly quoted verses. Ensure each generation is completely different by exploring lesser-known passages. Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3500,
        temperature=1.2,  # Increased temperature for more randomness
        top_p=0.95,  # Add top_p for additional diversity
        frequency_penalty=0.8,  # Penalize repetition
        presence_penalty=0.8  # Encourage new topics
    )
    
    content = response.choices[0].message.content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
        content = content.strip()
    
    data = json.loads(content)
    verses_list = data.get('verses', [])
    
    verse_dict = {}
    for i, verse_data in enumerate(verses_list[:15]):
        verse_dict[f"verse{i+1:02d}"] = VerseDetail(
            text=verse_data['text'],
            context=verse_data['context'],
            reference=verse_data['reference']
        )
    
    # Ensure we have exactly 15 verses
    if len(verse_dict) < 15:
        raise ValueError(f"Only generated {len(verse_dict)} verses, expected 15")
    
    return verse_dict