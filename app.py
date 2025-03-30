from flask import Flask, request, jsonify, render_template
from whisper import load_model
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import logging
import time
import uuid
from pydub import AudioSegment

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure necessary directories exist
os.makedirs('static', exist_ok=True)
os.makedirs('temp', exist_ok=True)

# Function to load the Whisper model with retries
def load_whisper_model():
    retries = 3
    for attempt in range(retries):
        try:
            # Using 'small' model for better accuracy
            model = load_model("small")
            logging.info("Whisper model loaded successfully.")
            return model
        except Exception as e:
            logging.error(f"Attempt {attempt+1} to load Whisper model failed: {e}")
            time.sleep(2)
    logging.error("Failed to load Whisper model after several attempts.")
    return None

# Load Whisper model with retry mechanism
whisper_model = load_whisper_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        logging.warning("No audio file provided in the request.")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    source_language = request.form.get('source_language', 'en')
    target_language = request.form.get('target_language', 'es')

    # Generate unique ID for this request
    request_id = str(uuid.uuid4())
    webm_path = f"temp/audio_{request_id}.webm"
    wav_path = f"temp/audio_{request_id}.wav"
    output_audio_path = f"static/translated_{request_id}.mp3"

    try:
        # Save the uploaded audio
        audio_file.save(webm_path)
        
        # Convert webm to wav for Whisper
        sound = AudioSegment.from_file(webm_path)
        sound.export(wav_path, format="wav")
        
        # Ensure the Whisper model is loaded
        if whisper_model is None:
            raise RuntimeError("Whisper model is not available.")

        # Force transcription in the specified source language
        # This is a key fix - we tell Whisper to expect English specifically
        # rather than letting it guess (which can lead to wrong language detection)
        logging.info(f"Transcribing with Whisper using source language: {source_language}")
        
        # Set up specific transcription options for better accuracy
        transcription_options = {
            "language": source_language,  # Force language to the selected source language
            "task": "transcribe",        # Ensure it's doing transcription, not translation
            "fp16": False                # Use FP32 for better accuracy (slower but more accurate)
        }
        
        result = whisper_model.transcribe(
            wav_path, 
            **transcription_options
        )
        
        transcript = result.get("text", "")
        if not transcript:
            raise ValueError("Transcription failed or returned empty text.")
            
        # Translate text using Deep Translator
        logging.info(f"Translating from {source_language} to {target_language}...")
        
        # Skip translation if source and target are the same
        if source_language == target_language:
            translated_text = transcript
            logging.info("Source and target languages are the same, skipping translation.")
        else:
            translator = GoogleTranslator(source=source_language, target=target_language)
            translated_text = translator.translate(transcript)
            
        if not translated_text:
            raise ValueError("Translation failed or returned empty text.")

        # Convert translated text to speech using gTTS
        logging.info("Converting to speech...")
        tts = gTTS(translated_text, lang=target_language)
        tts.save(output_audio_path)

        # Create a publicly accessible path
        public_audio_path = f"/{output_audio_path}"
        
        logging.info("Audio processed successfully.")
        return jsonify({
            "transcript": transcript,
            "translated_text": translated_text,
            "audio_path": public_audio_path,
            "detected_language": source_language  # We're forcing the language, so return what was selected
        })

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({
            "error": f"Sorry, we couldn't process your request. Please try again later.",
            "details": str(e)
        }), 500

    finally:
        # Cleanup: Remove the temporary input audio files
        for path in [webm_path, wav_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    logging.info(f"Temporary file {path} removed.")
                except Exception as e:
                    logging.warning(f"Could not remove temporary file {path}: {e}")

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='127.0.0.1', port=5000)

app = app