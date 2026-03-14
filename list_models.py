from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# This prints every model you can currently use
for m in client.models.list():
    print(m.name)