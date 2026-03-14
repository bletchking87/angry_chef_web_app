import os
import time
from dotenv import load_dotenv
from google import genai
import google.genai.errors as errors

# THE VITAL NEW IMPORTS
from elevenlabs.client import ElevenLabs
from elevenlabs import play 

# 1. LOAD THE SECRET VAULT
load_dotenv() 

# 2. INITIALIZE THE BRAIN AND THE VOICE
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
voice_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def get_recipe(ingredients):
    # The 'Personality' instructions
    instructions = "You are a passionate, loud Italian chef. Max 200 words."
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", # Use the stable 2.0 or 3.0 flash
        contents=f"{instructions} Ingredients: {ingredients}"
    )
    return response.text

def get_recipe_with_retry(ingredients):
    """The safety wrapper to handle 'Resource Exhausted' errors"""
    try:
        return get_recipe(ingredients)
    except errors.ClientError as e:
        # Check if it's specifically the "slow down" error
        if "429" in str(e):
            print("\n[CHEF]: Ma che cazzo! The kitchen is too busy! I need 30 seconds to breathe...")
            time.sleep(30)
            return get_recipe(ingredients) # Try one more time
        else:
            raise e # If it's a different error, let it crash so we can see why

# --- RUN TEST ---
if __name__ == "__main__":
ingredients = "A single egg, some flour, and a dream."
chef_response = get_recipe_with_retry(ingredients)
print(chef_response)

# To hear it (uncomment the lines below once you pick a voice):
# audio = voice_client.generate(text=result, voice="Giovanni", model="eleven_multilingual_v2")
# play(audio)