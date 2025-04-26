# Libraries
import datetime
import time
import sys
import webbrowser
import pyttsx3 # Converts text to voice (offline, unlike gTTS which needs internet).
import speech_recognition as sr # Listens to user speech and converts it to text using Google Speech API.
import pyautogui # GUI automation (not fully used here, but useful for interaction)
import os
import psutil #Helps get system resource usage like battery, CPU.
import json # Loads and parses .json files
import pickle # Used to load saved tokenizer and label encoder (from training).
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random # Performs random selection or generation from intents.json.
import numpy as np # Math operations for AI model

def get_nova_response(query):
    # (Import dependencies at the top as in main.py)

    # Load model and data (do this only once at the top)
    global model, tokenizer, label_encoder, data

    if not model:
        with open("intents.json") as file:
            data = json.load(file)
        model = load_model("chat_model.h5")
        tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
        label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

    # Core processing
    query = query.lower()
    
    # Intent prediction
    padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
    result = model.predict(padded_sequences)
    tag = label_encoder.inverse_transform([np.argmax(result)])[0]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

    return "Sorry, I didn't understand that."