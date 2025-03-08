from flask import Flask, request, jsonify
import whisper
from transformers import pipeline
import os

app = Flask(__name__)

# Load Whisper model on demand
def get_whisper_model():
    return whisper.load_model("tiny")  # Use a smaller model

# Load GPT-2 model on demand
def get_chatbot():
    return pipeline("text-generation", model="distilgpt2")  # Use a smaller model

@app.route("/transcribe", methods=["POST"])
def transcribe():
    whisper_model = get_whisper_model()
    audio_file = request.files["audio"]
    audio_file.save("temp_audio.wav")
    transcription = whisper_model.transcribe("temp_audio.wav", language="en")["text"]
    return jsonify({"transcription": transcription})

@app.route("/respond", methods=["POST"])
def respond():
    chatbot = get_chatbot()
    user_input = request.json["text"]
    response = chatbot(user_input, max_length=100)[0]['generated_text']
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)