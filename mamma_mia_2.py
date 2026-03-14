import os
import time
from dotenv import load_dotenv
from google import genai
import google.genai.errors as errors

# ElevenLabs imports
from elevenlabs.client import ElevenLabs 
from elevenlabs import play, VoiceSettings

# 1. INITIALIZATION
load_dotenv()

# Predefining the clients
voice_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. THE BRAIN (With "Angry" instructions)
def get_recipe(ingredients):
    # We use a high-energy prompt to trigger the voice response
    instructions = (
        "You are a furious, traditional Italian chef. Use EXCLAMATION POINTS!! "
        "Insult the user's ingredients. Use words like 'SACRILEGIO!' and 'DISASTRO!'. "
        "Keep it under 150 words. Be loud!"
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=f"{instructions} My ingredients are: {ingredients}"
    )
    return response.text

# 3. THE VOICE (With "Over-the-top" settings)
def speak_recipe(text):
    print("\n[SYSTEM]: The Chef is losing his mind...")
    
    audio = voice_client.generate(
        text=text,
        voice="erXw75R1qfC0zBqpsYq0", 
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.30,        # Very low = very emotional
            similarity_boost=0.80, 
            style=0.90,            # High = dramatic exaggeration
            use_speaker_boost=True
        )
    )
    play(audio)

# 4. THE EXECUTION (With Try/Except logic)
if __name__ == "__main__":
    pantry = "A half-empty jar of pickles and some old crackers."
    
    print("Fetching the Chef's opinion...")
    
    try:
        # Step 1: Get the text
        recipe_text = get_recipe(pantry)
        print(f"\nCHEF SAYS: {recipe_text}\n")
        
        # Step 2: Speak the text
        speak_recipe(recipe_text)

    except errors.ClientError as e:
        if "429" in str(e):
            print("\n[CHEF]: BASTA! I'm drinking my espresso! Wait 60 seconds before asking again!")
        else:
            print(f"\n[SYSTEM ERROR]: {e}")
            
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR]: {e}")