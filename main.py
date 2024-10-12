import sounddevice as sd
import numpy as np
import json
from vosk import Model, KaldiRecognizer
import requests
import pyttsx3
import threading

# Load the Vosk model
model = Model("./vosk_model")

# Set up the recognizer
samplerate = 16000
rec = KaldiRecognizer(model, samplerate)

can_listen = True

# Initialize the TTS engine
engine = pyttsx3.init()

def send_prompt_over_network(msg):
    request = requests.post("http://192.168.0.3:11434/api/generate", data='{"model" : "llama3.1", "prompt" : "' + msg + '", "stream": false}')
    response = request.json()
    print(response)
    
    # Extract the response text
    response_text = response["response"]
    
    # Speak the response using TTS in a separate thread
    speak_text(response_text)

def speak_text(text):
    can_listen = False
    engine.say(text)
    engine.runAndWait()
    can_listen = True

# Callback function for the stream
def callback(indata, frames, time, status):
    if status:
        print(status)
    if rec.AcceptWaveform(bytes(indata)):
        result = json.loads(rec.Result())
        if result['text']:
            print("Final result:", result['text'])
            send_prompt_over_network(result["text"])
    else:
        partial = json.loads(rec.PartialResult())
        if partial['partial']:
            print("Partial result:", partial['partial'], end='\r')

# Start the microphone stream
print("Listening... (Press Ctrl+C to stop)")
try:
    if can_listen:
        with sd.RawInputStream(samplerate=samplerate, blocksize=4000, dtype='int16', channels=1, callback=callback):
            while True:
                pass
except KeyboardInterrupt:
    print("\nStopping...")

print("Finished.")