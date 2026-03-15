import streamlit as st
import os
from google import genai
from elevenlabs.client import ElevenLabs
import httpx 


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

# Wrap EVERYTHING in a form so "Enter" triggers the button
with st.form("chef_form"):
    if mode == "Create Recipe":
        st.subheader("What's in your fridge, you amateur?")
        user_input = st.text_input("List ingredients:")
        # Updated prompt strategy
        accent_instructions = (
    "RULES FOR ACCENT: "
    "1. Only add an 'a' at the end of words ending in a hard consonant if t(e.g., 'cook-a the meat-a' BUT 'pot of water', 'pasta and-a cheese-a). "
    "2. NEVER add vowels inside a word or between two vowels. "
    "3. Keep 70 percent of the words in standard English so it remains readable. "
    "4. Use 'thees-a' for 'this' and 'ees-a' for 'is'—but do not overdo it."
)
        prompt_text = f"Role: Grumpy Italian Chef. Task: {user_input}. {accent_instructions}"
        
        
       

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