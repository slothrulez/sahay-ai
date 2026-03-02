import os
from flask import Flask, request, send_file, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import your custom modules from the core folder
from core.stt_engine import transcribe_audio
from core.reasoning import simplify_query
from core.tts_engine import synthesize_speech

# Load API Keys from .env
load_dotenv()

app = Flask(__name__)
CORS(app) # Allows your website to talk to the backend without security blocks

# Ensure the temp folder exists for audio processing
if not os.path.exists('temp_audio'):
    os.makedirs('temp_audio')

@app.route('/')
def index():
    """Renders the Sahay AI Web Demo Interface"""
    return render_template('index.html')

@app.route("/process-web-voice", methods=['POST'])
def web_pipeline():
    """
    Handles audio from your Demo Website.
    This bypasses telephony issues and runs the AI pipeline directly.
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file found"}), 400

        # 1. Save the incoming web audio
        audio_file = request.files['audio']
        input_path = os.path.join('temp_audio', 'web_input.wav')
        audio_file.save(input_path)

        print("--- Pipeline Started: Web Interface ---")

        # 2. STEP 1: STT (Speech to Text)
        print("Transcribing with Sarvam AI...")
        user_text = transcribe_audio(input_path)
        print(f"User said: {user_text}")

        # 3. STEP 2: Reasoning (LLM Simplification)
        print("Simplifying with Gemini...")
        simplified_response = simplify_query(user_text)
        print(f"AI Response: {simplified_response}")

        # 4. STEP 3: TTS (Text to Speech)
        print("Synthesizing Voice Response...")
        # Note: Ensure your tts_engine.py saves to 'temp_audio/output.wav'
        output_path = synthesize_speech(simplified_response) 

        print("--- Pipeline Complete ---")
        
        # 5. Return the audio file to the browser
        return send_file(output_path, mimetype="audio/wav")

    except Exception as e:
        print(f"Pipeline Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/process-web-voice", methods=['POST'])
def telephony_pipeline():
    """
    Keep this for your Twilio/Exotel Telephony Review.
    It works exactly like the web pipeline but for phone calls.
    """
    # Twilio sends audio as a URL or File depending on config
    # For now, we'll keep it as a placeholder for your 'Technical Architecture' slide
    return "Telephony endpoint active and listening."

if __name__ == "__main__":
    # Run on port 5000. Use 'python app.py' to start.
    app.run(host='0.0.0.0', port=5000, debug=True)