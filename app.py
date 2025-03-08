import os
from flask import Flask, request, jsonify
import whisper
from transformers import pipeline

import scipy.io.wavfile as wav
import numpy as np
import ctypes
try:
    import sounddevice as sd
except OSError as e:
    print("PortAudio library not found. Audio recording will not work.")
    sd = None
    
# Manually specify the path to libc (required for Whisper on Windows)
if os.name == "nt":  # Check if the OS is Windows
    libc_path = "msvcrt.dll"  # This is the standard libc library on Windows
    ctypes.CDLL(libc_path)

app = Flask(__name__)

# Load Whisper model
whisper_model = whisper.load_model("base")

# Load GPT-2 model
chatbot = pipeline("text-generation", model="gpt2")

# Speech-to-text endpoint
@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Save the uploaded audio file
    audio_file = request.files["audio"]
    audio_file.save("temp_audio.wav")

    # Transcribe the audio
    transcription = whisper_model.transcribe("temp_audio.wav", language="en")["text"]
    return jsonify({"transcription": transcription})

# Response generation endpoint
@app.route("/respond", methods=["POST"])
def respond():
    user_input = request.json["text"]
    response = chatbot(user_input, max_length=100)[0]['generated_text']
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host="0.0.0.0", port=port)