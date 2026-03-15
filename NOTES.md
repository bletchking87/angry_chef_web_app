### This is a log of the things I have built and integrated into the Angry Chef Web App, along with the timings. 

14th March:
- Created Streamlit application and hooked up the Gemini and ElevenLabs APIs.
- Had to add a timeout with httpx - this allowed the audio generation to take the necessary seconds without a TimeOut Error
- It is easier with Streamlit to **change the main script locally and keep the name** than set up a new application where the main script changes name. You have to add all the secrets again otherwise.

15th March:
- Added sidebar and added an expander for session history so the sidebar doesn't grow indefinitely. Though, with analytics at the top, though this will be revised, because for your average user the analytics don't matter.
- Added Google Sheets for data logging, and enabled Sheets and Drive API. Gave necessary permissions to the service account.
