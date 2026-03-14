import streamlit as st
import os
from google import genai
from elevenlabs.client import ElevenLabs

# 1. Access Secrets
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")

if not GEMINI_KEY or not ELEVEN_KEY:
    st.error("API Keys missing in Streamlit Secrets!")
    st.stop()

# 2. Initialize Clients
gen_client = genai.Client(api_key=GEMINI_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_KEY)

# 3. Sidebar Configuration
st.sidebar.title("👨‍🍳 Chef's Control Panel")
mode = st.sidebar.radio(
    "Select Task:",
    ["Create Recipe", "Dish History", "Just Insult Me"]
)

# 4. Main UI Logic
st.title("🤌 The Angry Italian Chef")

if mode == "Create Recipe":
    st.subheader("What's in your fridge, you amateur?")
    user_input = st.text_input("List ingredients (e.g., eggs, old cheese, disappointment):")
    prompt = f"You are a grumpy Italian chef. Create a legitimate recipe using: {user_input}. Be insulting about their ingredients but give a real recipe. Write the recipe as Chef Antonino Grumpo. Use heavy Italian-English phonetic spelling (e.g., 'thees-a', 'cook-a the pasta') to ensure an over-the-top Italian accent when read by a text-to-speech engine."

elif mode == "Dish History":
    st.subheader("Education for the uncultured...")
    user_input = st.text_input("Enter a dish name:")
    prompt = f"You are a grumpy Italian chef. Explain the history of {user_input}. Make it dramatic, slightly inaccurate, and very insulting. Write the recipe as Chef Antonino Grumpo. Use heavy Italian-English phonetic spelling (e.g., 'thees-a', 'cook-a the pasta') to ensure an over-the-top Italian accent when read by a text-to-speech engine."

else:
    st.subheader("Who needs to hear the truth?")
    user_input = st.text_input("Target name:")
    prompt = f"Give a ridiculous, accented Italian insult to {user_input}."

# 5. Execution
if st.button("MAKE THE CHEF SPEAK"):
    if not user_input:
        st.warning("Input something first, you donkey!")
    else:
        with st.spinner("The Chef is thinking... and he's not happy..."):
            # A. Generate Text
            response = gen_client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            chef_text = response.text
            st.write(chef_text)

            # B. Generate Audio (Using a stable Giovanni/Antoni ID)
            audio = eleven_client.generate(
                text=chef_text,
                voice="s2wvuS7SwITYg8dqsJdn", # Giovanni
                model="eleven_multilingual_v2"
            )
            st.audio(bytes(audio), format="audio/mp3")