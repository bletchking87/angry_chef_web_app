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

# Initialize Clients
gen_client = genai.Client(api_key=GEMINI_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_KEY)

# --- 2. INITIALIZE HISTORY (LEVEL 1) ---
if "chef_history" not in st.session_state:
    st.session_state.chef_history = []

# --- 3. SIDEBAR CONFIGURATION ---
st.sidebar.title("👨‍🍳 Chef's Control Panel")
mode = st.sidebar.radio(
    "Select Task:",
    ["Create Recipe", "Dish History", "Just Insult Me"]
)

# Show history in the sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("📜 Past Insults")
    for entry in reversed(st.session_state.chef_history):
        with st.expander(f"{entry['mode']}: {entry['input'][:15]}..."):
            st.write(entry['recipe'])

# --- 4. MAIN UI LOGIC ---
st.title("🤌 The Angry Italian Chef")

# Wrap EVERYTHING in a form so "Enter" triggers the button
with st.form("chef_form"):
    if mode == "Create Recipe":
        st.subheader("What's in your fridge, you amateur?")
        user_input = st.text_input("List ingredients:")
        prompt_text = f"You are a grumpy Italian chef. Create a legitimate recipe using: {user_input}. Be insulting but give a real recipe. Use heavy phonetic Italian-English (e.g., 'thees-a', 'pasta-a')."

    elif mode == "Dish History":
        st.subheader("Education for the uncultured...")
        user_input = st.text_input("Enter a dish name:")
        prompt_text = f"Explain the history of {user_input} as a grumpy Italian chef. Be dramatic and insulting. Use heavy phonetic Italian-English."

    else:
        st.subheader("Who needs to hear the truth?")
        user_input = st.text_input("Target name:")
        prompt_text = f"Give a ridiculous, accented Italian insult to {user_input}."

    # The Submit Button
    submitted = st.form_submit_button("MAKE THE CHEF SPEAK")

# --- 5. EXECUTION ---
if submitted:
    if not user_input:
        st.warning("Input something first, you donkey!")
    else:
        with st.spinner("The Chef is thinking... and he's not happy..."):
            try:
                # A. Generate Text
                response = gen_client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt_text
                )
                chef_text = response.text
                st.write(chef_text)

                # B. Generate Audio
                audio = eleven_client.generate(
                    text=chef_text,
                    voice="s2wvuS7SwITYg8dqsJdn", 
                    model="eleven_multilingual_v2"
                )
                
                # Convert generator to bytes for st.audio
                audio_data = b"".join(list(audio))
                st.audio(audio_data, format="audio/mp3")

                # C. Save to History
                st.session_state.chef_history.append({
                    "mode": mode,
                    "input": user_input,
                    "recipe": chef_text
                })

            except Exception as e:
                st.error(f"The kitchen is on fire! Error: {e}")