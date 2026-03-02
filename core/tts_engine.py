import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def synthesize_speech(text, language_code="ta-IN"): # Defaulted to Hindi for Sahay
    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "speaker": "abhilash", 
        "model": "bulbul:v2"
    }
    
    headers = {
        "Content-Type": "application/json", 
        "api-subscription-key": SARVAM_API_KEY
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        # --- DEBUGGING LAYER ---
        # print(f"DEBUG: Sarvam TTS Response: {result}")

        # Sarvam Bulbul:v2 returns 'audio_codes' which is a list of base64 strings
        audio_base64 = result.get('audio_codes', [None])[0]

        if not audio_base64:
            # Fallback check for older 'audios' key or 'audio' key
            audio_base64 = result.get('audios', [None])[0] or result.get('audio')

        if audio_base64:
            # 1. Decode the base64 string into actual audio bytes
            audio_bytes = base64.b64decode(audio_base64)
            
            # 2. Save it as a wav file for the browser to play
            output_path = os.path.join("temp_audio", "output.wav")
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            
            return output_path
        else:
            print(f"TTS Error: No audio data in response. Full response: {result}")
            return None

    except Exception as e:
        print(f"TTS Pipeline Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Quick Test
    path = synthesize_speech("Namaste, main Sahay AI hoon.")
    print(f"Audio saved at: {path}")