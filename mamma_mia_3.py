import streamlit as st
import os
from google import genai
from elevenlabs.client import ElevenLabs
import httpx 
import datetime


# 1. Access Secrets
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")

if not GEMINI_KEY or not ELEVEN_KEY:
    st.error("API Keys missing in Streamlit Secrets!")
    st.stop()

# Initialize Clients
gen_client = genai.Client(api_key=GEMINI_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_KEY,
    httpx_client=httpx.Client(timeout=120.0) # Gives the Chef 2 minutes to talk
)

# --- 2. INITIALIZE HISTORY ---
if "chef_history" not in st.session_state:
    st.session_state.chef_history = []


# --- 3. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("👨‍🍳 Chef's Control Panel")
    
    # DIAGNOSTICS
    st.markdown("### 📊 System Diagnostics")
    st.caption("Infrastructure: High Availability")
    
    if st.session_state.chef_history:
        total_chars = sum(len(h['recipe']) for h in st.session_state.chef_history)
        # Metrics look great in the sidebar
        st.metric("Chars Synthesized", f"{total_chars:,}")
    
    st.markdown("---")
    
    # INPUT CONTROLS
    mode = st.radio(
        "Select Task:",
        ["Create Recipe", "Dish History", "Just Insult Me"]
    )
    
    st.markdown("---")
    
    # HISTORY AT THE BOTTOM (It can grow indefinitely)
    st.subheader("📜 Past Insults")
    for entry in reversed(st.session_state.chef_history):
        # The expander keeps the sidebar from becoming a mile long
        with st.expander(f"{entry['mode']}: {entry['input'][:15]}..."):
            st.write(entry['recipe'])
# --- 4. MAIN UI LOGIC ---
st.title("🤌 The Angry Italian Chef")

# --- GLOBAL PERSONA CONSTRAINTS ---
accent_instructions = (
    "ACT AS A GRUMPY ITALIAN CHEF. "
    "1. Keep 90% of the words standard English for clarity. "
    "2. Be rude, impatient, and judgmental."
)



# Wrap EVERYTHING in a form so "Enter" triggers the button
with st.form("chef_form"):
    if mode == "Create Recipe":
        st.subheader("What's in your fridge, you amateur?")
        user_input = st.text_input("List ingredients:")
        # Updated prompt strategy
        prompt_text = f"Role: Grumpy Italian Chef. Task: {user_input}. {accent_instructions}"
        
    elif mode == "Dish History":
        st.subheader("Education for the uncultured...")
        user_input = st.text_input("Enter a dish name:")
        prompt_text = f"Explain the history of {user_input} as a grumpy Italian chef. {accent_instructions}."

    else:
        st.subheader("Who needs to hear the truth?")
        user_input = st.text_input("Target name:")
        prompt_text = f"Give a ridiculous, accented Italian insult to {user_input}. {accent_instructions}"

    # The Submit Button
    submitted = st.form_submit_button("MAKE THE CHEF SPEAK")

# --- 5. EXECUTION ---

if submitted:
    # Inside your 'if submitted' block:
    full_prompt = f"{accent_instructions}\n\nUSER TASK: {user_input}\nMODE: {mode}"
    if not user_input:
        st.warning("Input something first, you donkey!")
    else:
        with st.spinner("The Chef is screaming into the microphone..."):
            try:
                # A. Generate Text (Gemini)
               
                response = gen_client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt_text + " Keep it brief, under 150 words!"
                )
                chef_text = response.text
                st.write(chef_text)

                # B. Generate Audio (ElevenLabs)
                # Using turbo for speed to prevent Streamlit timeouts
                audio_stream = eleven_client.generate(
                    text=chef_text,
                    voice="s2wvuS7SwITYg8dqsJdn", 
                    model="eleven_turbo_v2_5" 
                )
                
                # THE FIX: Convert the stream into solid data
                audio_data = b"".join(list(audio_stream))
                
                if audio_data:
                    st.audio(audio_data, format="audio/mp3")
                else:
                    st.error("The Chef's voice was lost! Check your ElevenLabs dashboard.")

                # C. Save to History (Level 1 Memory)
                st.session_state.chef_history.append({
                    "mode": mode,
                    "input": user_input,
                    "recipe": chef_text
                })

            except Exception as e:
                st.error(f"The kitchen is on fire! Error: {e}")