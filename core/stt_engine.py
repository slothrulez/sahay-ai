import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get your API key from the .env file
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def transcribe_audio(file_path):
    """
    Sends audio to Sarvam AI and extracts the transcript.
    Includes error handling to prevent the 'KeyError: transcript' crash.
    """
    url = "https://api.sarvam.ai/speech-to-text"
    
    if not SARVAM_API_KEY:
        return "Error: SARVAM_API_KEY not found in .env"

    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }

    # Opening the file in binary mode
    try:
        with open(file_path, 'rb') as audio_file:
            files = {
                'file': (os.path.basename(file_path), audio_file, 'audio/wav')
            }
            # Add the language code (defaulting to Malayalam for Sahay)
            data = {
                'language_code': 'ml-IN',
                'model': 'saaras:v3'
            }

            response = requests.post(url, headers=headers, files=files, data=data)
            
            # --- DEBUGGING LAYER ---
            # This prints the raw response to your terminal so you can see the fix
            result = response.json()
            print(f"DEBUG: Sarvam Raw Response: {result}")

            if response.status_code == 200:
                # Use .get() to prevent 'KeyError' crashes
                transcript = result.get('transcript') or result.get('text')
                
                if transcript:
                    return transcript
                else:
                    return "Error: Response received but no transcript key found."
            else:
                return f"Error {response.status_code}: {result.get('error', 'Unknown Error')}"

    except Exception as e:
        return f"Pipeline Connection Error: {str(e)}"

if __name__ == "__main__":
    # Quick local test
    print(transcribe_audio("temp_audio/web_input.wav"))