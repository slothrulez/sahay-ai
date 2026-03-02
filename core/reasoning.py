import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def simplify_query(user_text):
    headers = {'Content-Type': 'application/json'}
    
    try:
        # 1. ASK GOOGLE: "What models do I actually have access to?"
        models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        models_resp = requests.get(models_url)
        models_data = models_resp.json()
        
        # Find the first model that supports 'generateContent'
        available_models = [
            m['name'] for m in models_data.get('models', []) 
            if 'generateContent' in m.get('supportedGenerationMethods', [])
        ]
        
        if not available_models:
            print("CRITICAL: No models found for this API key.")
            return "Technical error: No models available."

        # 2. Pick the best available (usually Flash or Pro)
        # We look for 'flash' first as it's faster for voice
        selected_model = next((m for m in available_models if "flash" in m), available_models[0])
        print(f"DEBUG: Auto-selected Model: {selected_model}")

        # 3. USE THE SELECTED MODEL
        # Note: selected_model already contains the "models/" prefix
        url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
        
        prompt_text = f"You are Sahay AI. Provide a simple answer(maximum 500 characters total) in the SAME language as the user's question: {user_text}"
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Generation Failed: {result}")
            return "Maaf kijiye, system me thodi deri hai."

    except Exception as e:
        print(f"Discovery Error: {str(e)}")
        return "Reasoning system offline."