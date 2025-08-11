import openai
import random
from typing import Dict
from app.core.config import settings

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=settings.openai_api_key)

# Function to generate random verses using OpenAI GPT-4
def generate_random_verses() -> Dict[str, str]:
    prompt = """Generate exactly 15 truly random Bible verses from various books of the Bible. 
    
    Requirements:
    - Each verse must include the complete biblical reference at the end (Book Chapter:Verse)
    - Use this exact format: "Verse text - Book Chapter:Verse"
    - Only use actual Bible verses from the Old Testament and New Testament
    - DO NOT start with Genesis 1:1 - ensure proper randomization across all books
    - Include verses from different books (Psalms, Proverbs, Ecclesiastes, Isaiah, Matthew, John, Romans, etc.)
    - Ensure true randomness - don't default to the most famous or first verses
    - Provide each verse on a separate line
    - Do not number the verses
    
    Example format:
    For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life. - John 3:16"""

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a biblical scholar who provides truly random Bible verses with proper citations. Always include the complete biblical reference (Book Chapter:Verse) at the end of each verse using the format: 'Verse text - Book Chapter:Verse'. Only provide actual Bible verses from the Holy Scripture. Ensure verses are randomly selected from throughout the Bible - don't default to famous verses or Genesis 1:1. Each time you're asked, generate a completely different set of random verses."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature
        )
        
        # Extract verses from the response text
        verses_text = response.choices[0].message.content.strip()
        
        # Split the response into individual verses (assuming each verse is on a new line)
        verses = [verse.strip() for verse in verses_text.split("\n") if verse.strip()]
        
        # Filter out empty strings and numbering if present
        filtered_verses = []
        for verse in verses:
            # Remove leading numbers and dots/dashes if present
            cleaned_verse = verse.lstrip("0123456789.- ").strip()
            if cleaned_verse and len(cleaned_verse) > 20:  # Ensure it's a meaningful verse with reference
                filtered_verses.append(cleaned_verse)
        
        # Create dictionary with verse01 to verse15 keys
        verse_dict = {}
        for i in range(15):
            if i < len(filtered_verses):
                verse_dict[f"verse{i+1:02d}"] = filtered_verses[i]
            else:
                # If we don't have enough verses, stop here
                break
        
        return verse_dict
        
    except Exception as e:
        print(f"Error generating verses: {str(e)}")
        raise e