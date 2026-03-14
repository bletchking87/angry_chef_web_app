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
    prompt = f"You are a grumpy Italian chef. Create a legitimate recipe using: {user_input}. Be insulting about their ingredients but give a real recipe."

elif mode == "Dish History":
    st.subheader("Education for the uncultured...")
    user_input = st.text_input("Enter a dish name:")
    prompt = f"You are a grumpy Italian chef. Explain the history of {user_input}. Make it dramatic, slightly inaccurate, and very insulting."

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
                model="gemini-1.5-flash", 
                contents=prompt
            )
            chef_text = response.text
            st.write(chef_text)

            # B. Generate Audio (Using a stable Giovanni/Antoni ID)
            audio = eleven_client.generate(
                text=chef_text,
                voice="zcAOhNBS3c14rBihAFp1", # Giovanni
                model="eleven_multilingual_v2"
            )
            st.audio(audio, format="audio/mp3")google.genai.errors.ClientError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/angry_chef_web_app/mamma_mia_3.py", line 50, in <module>
    response = gen_client.models.generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/models.py", line 5709, in generate_content
    response = self._generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/models.py", line 4371, in _generate_content
    response = self._api_client.request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/_api_client.py", line 1401, in request
    response = self._request(http_request, http_options, stream=False)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/_api_client.py", line 1237, in _request
    return self._retry(self._request_once, http_request, stream)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/tenacity/__init__.py", line 470, in __call__
    do = self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/tenacity/__init__.py", line 371, in iter
    result = action(retry_state)
             ^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/tenacity/__init__.py", line 413, in exc_check
    raise retry_exc.reraise()
          ^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/tenacity/__init__.py", line 184, in reraise
    raise self.last_attempt.result()
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 449, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
File "/home/adminuser/venv/lib/python3.12/site-packages/tenacity/__init__.py", line 473, in __call__
    result = fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/_api_client.py", line 1214, in _request_once
    errors.APIError.raise_for_response(response)
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/errors.py", line 134, in raise_for_response
    cls.raise_error(response.status_code, response_json, response)
File "/home/adminuser/venv/lib/python3.12/site-packages/google/genai/errors.py", line 159, in raise_error
    raise ClientError(status_code, response_json, response)