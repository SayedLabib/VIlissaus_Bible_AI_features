import openai
import json
import random
import time
import asyncio
import concurrent.futures
from typing import Dict, List, Any, Tuple
from app.core.config import settings
from app.services.Daily_verse_generation.Verse_generation_schema import VerseDetail, PrayerDetail

client = openai.OpenAI(api_key=settings.openai_api_key)

def generate_verses_batch(batch_num: int, batch_size: int = 5) -> List[Tuple[str, str, str]]:
    """Generate a batch of Bible verses (5 at a time)"""
    print(f"=" * 50)
    print(f"GENERATING VERSES BATCH {batch_num}")
    print(f"=" * 50)
    
    random_seed = int(time.time() * 1000) + random.randint(1, 10000)
    bible_versions = ["KJV", "NIV", "ESV", "NLT"]
    primary_versions = random.sample(bible_versions, k=2)
    
    print(f"Random seed: {random_seed}")
    print(f"Primary versions: {primary_versions}")
    
    prompt = f"""Generate exactly {batch_size} unique Bible verses.

CRITICAL: Return ONLY a valid JSON array of arrays that Python json.loads() can parse.

REQUIRED FORMAT - Return EXACTLY this format and nothing else:
[
  ["verse text", "explanation", "Book Chapter:Verse"],
  ["verse text", "explanation", "Book Chapter:Verse"]
]

JSON RULES (EXTREMELY IMPORTANT):
- ONLY return a JSON array - NO markdown, NO code blocks, NO explanations
- Use DOUBLE QUOTES for all JSON strings, never single quotes
- DO NOT include ```json or ``` around your response
- First character must be [, last character must be ]
- Use apostrophes inside text instead of quotes

CONTENT GUIDELINES:
- Include lesser-known books: Habakkuk, Zephaniah, Malachi, Obadiah, Philemon, Jude, etc.
- 60% Old Testament, 40% New Testament
- Use versions: {primary_versions[0]}, {primary_versions[1]}, ESV, NLT
- Random chapters, not just chapter 1

Batch: {batch_num}
Seed: {random_seed}"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are a JSON generator. Return ONLY valid JSON arrays. No markdown. No explanations. Just valid JSON that starts with [ and ends with ]. No exceptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    content = response.choices[0].message.content.strip()
    print(f"Raw response first 100 chars: {content[:100]}...")
    
    # Remove any markdown wrapper if present
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
        content = content.strip()
    
    try:
        parsed = json.loads(content)
        print(f"✓ Batch {batch_num}: Successfully parsed {len(parsed)} verses")
        return parsed
    except json.JSONDecodeError as e:
        print(f"✗ JSON error in batch {batch_num}: {e}")
        # Return default verses for this batch as fallback
        default_verses = []
        for i in range(batch_size):
            default_verses.append([
                f"Default verse text for batch {batch_num}, item {i+1}",
                f"This is a fallback verse due to JSON parsing error in batch {batch_num}",
                f"Joshua 1:{batch_num}{i+1} NIV"
            ])
        return default_verses


def generate_prayers_batch(batch_num: int, batch_size: int = 5) -> List[Tuple[str, str]]:
    """Generate a batch of prayers (5 at a time)"""
    print(f"=" * 50)
    print(f"GENERATING PRAYERS BATCH {batch_num}")
    print(f"=" * 50)
    
    random_seed = int(time.time() * 1000) + random.randint(1, 10000)
    
    prompt = f"""Generate exactly {batch_size} unique prayers.

CRITICAL: Return ONLY a valid JSON array of arrays that Python json.loads() can parse.

REQUIRED FORMAT - Return EXACTLY this format and nothing else:
[
  ["Prayer Title", "Complete prayer text"],
  ["Prayer Title", "Complete prayer text"]
]

JSON RULES (EXTREMELY IMPORTANT):
- ONLY return a JSON array - NO markdown, NO code blocks, NO explanations
- Use DOUBLE QUOTES for all JSON strings, never single quotes
- DO NOT include ```json or ``` around your response
- First character must be [, last character must be ]
- Use apostrophes inside text instead of quotes

CONTENT GUIDELINES:
- Each prayer should be 3-5 sentences
- Include prayers for: guidance, strength, peace, healing, forgiveness, etc.
- First element is the prayer title/name
- Second element is the complete prayer text
- Make prayers personal and practical

Batch: {batch_num}
Seed: {random_seed}"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are a JSON generator. Return ONLY valid JSON arrays. No markdown. No explanations. Just valid JSON that starts with [ and ends with ]. No exceptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    content = response.choices[0].message.content.strip()
    print(f"Raw response first 100 chars: {content[:100]}...")
    
    # Remove any markdown wrapper if present
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
        content = content.strip()
    
    try:
        parsed = json.loads(content)
        print(f"✓ Batch {batch_num}: Successfully parsed {len(parsed)} prayers")
        return parsed
    except json.JSONDecodeError as e:
        print(f"✗ JSON error in batch {batch_num}: {e}")
        # Return default prayers for this batch as fallback
        default_prayers = []
        for i in range(batch_size):
            default_prayers.append([
                f"Default Prayer {batch_num}-{i+1}",
                f"Heavenly Father, please guide us in your ways. Help us to trust in your perfect plan for our lives. Give us strength to face our challenges. In Jesus' name, Amen."
            ])
        return default_prayers


def generate_random_verses() -> Dict[str, Any]:
    """Generate 15 verses and 15 prayers using concurrent API calls"""
    
    print("\n" + "=" * 60)
    print("STARTING VERSE AND PRAYER GENERATION WITH BATCHES")
    print("=" * 60 + "\n")
    
    all_verses = []
    all_prayers = []
    
    # Use concurrent execution for faster processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Submit verse generation tasks (3 batches of 5 verses)
        verse_futures = [executor.submit(generate_verses_batch, i+1) for i in range(3)]
        
        # Submit prayer generation tasks (3 batches of 5 prayers)
        prayer_futures = [executor.submit(generate_prayers_batch, i+1) for i in range(3)]
        
        # Collect verse results
        for future in concurrent.futures.as_completed(verse_futures):
            batch_result = future.result()
            all_verses.extend(batch_result)
            
        # Collect prayer results
        for future in concurrent.futures.as_completed(prayer_futures):
            batch_result = future.result()
            all_prayers.extend(batch_result)
    
    print(f"\n✓ Total verses collected: {len(all_verses)}")
    print(f"✓ Total prayers collected: {len(all_prayers)}")
    
    # Create result dictionary in the exact format required
    result = {}
    
    # Process verses
    for i in range(min(15, len(all_verses))):
        verse = all_verses[i]
        result[f"verse{i+1:02d}"] = VerseDetail(
            text=verse[0],
            context=verse[1],
            reference=verse[2]
        )
    
    # Process prayers
    for i in range(min(15, len(all_prayers))):
        prayer = all_prayers[i]
        result[f"prayer{i+1:02d}"] = PrayerDetail(
            text=prayer[0],
            context=prayer[1]
        )
    
    # Ensure we have exactly 15 of each
    # Pad with defaults if needed
    for i in range(len(all_verses), 15):
        result[f"verse{i+1:02d}"] = VerseDetail(
            text="The Lord is my shepherd; I shall not want.",
            context="This verse reminds us that God provides and cares for us like a shepherd cares for his sheep.",
            reference="Psalm 23:1 KJV"
        )
    
    for i in range(len(all_prayers), 15):
        result[f"prayer{i+1:02d}"] = PrayerDetail(
            text="Prayer for Daily Guidance",
            context="Heavenly Father, guide my steps today. Show me the path You have prepared for me and give me wisdom to follow it. Help me to trust in Your perfect plan even when I don't understand. In Jesus' name, Amen."
        )
    
    print("\n" + "=" * 60)
    print("FINAL RESULT SUMMARY")
    print("=" * 60)
    print(f"Total keys: {len(result)}")
    print(f"Verses: {len([k for k in result.keys() if k.startswith('verse')])}")
    print(f"Prayers: {len([k for k in result.keys() if k.startswith('prayer')])}")
    print("=" * 60 + "\n")
    
    return result
