# Libraries
import datetime
import time
import sys
import webbrowser
import pyttsx3 # Converts text to voice (offline, unlike gTTS which needs internet).
import speech_recognition as sr # Listens to user speech and converts it to text using Google Speech API.
import pyautogui # GUI automation (not fully used here, but useful for interaction)
from gtts import gTTS
import os
import uuid
import psutil #Helps get system resource usage like battery, CPU.
import json # Loads and parses .json files
import pickle # Used to load saved tokenizer and label encoder (from training).
from tensorflow.keras.models import load_model # Loads your trained NLP model to understand user intent.
from tensorflow.keras.preprocessing.sequence import pad_sequences # Prepare user input for the model
import random # Performs random selection or generation from intents.json.
import numpy as np # Math operations for AI model

# AI Model Loading
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)


# Text-to-Speech Setup
engine = pyttsx3.init("nsss")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[18].id)
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"static/{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

# 
def command():
    """Listens to user speech and converts it to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for background noise
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
        return "None"
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return "None"

def cal_day():
    """Returns the current day of the week"""
    day_dict = {
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"
    }
    return day_dict[datetime.datetime.today().weekday()]

def wishMe():
    """Greets the user with the current day and time"""
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()

    if 9 <= hour <= 12:
        speak(f"Good morning Kabeer, it's {day} and the time is {t}")
    elif 12 <= hour <= 16:
        speak(f"Good afternoon Kabeer, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Kabeer, it's {day} and the time is {t}")

def social_media(command):
    """Opens social media websites based on voice command"""
    if 'facebook' in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("Opening Discord")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is")
    week = {
        "monday": "Boss, from 9:00 AM to 9:50 AM you have Algorithm class, from 10:00 AM to 11:59 AM you have a Time Management session.",
        "tuesday": "Boss, from 9:00 AM to 9:50 AM you have Web Development class, from 10:00 AM to 11:59 AM you have a Project Discussion.",
        "wednesday": "Boss, from 9:00 AM to 9:50 AM you have Java class, from 10:00 AM to 11:59 AM you have a Group Presentation.",
        "thursday": "Boss, from 9:00 AM to 9:50 AM you have Organization Behavior class, from 10:00 AM to 11:59 AM you have a Research Workshop.",
        "friday": "Boss, from 9:00 AM to 9:50 AM you have a full day of classes, including Advanced Python and Data Science.",
        "saturday": "Boss, from 9:00 AM to 9:50 AM you have a more relaxed day, with a Seminar on Entrepreneurship.",
        "sunday": "Boss, today is a holiday, but feel free to work on personal projects or relax!"
    }
    if day in week.keys():
        speak(week[day])
    else:
        speak("Sorry Boss, I couldn't find your schedule for today.")

def open_application(query):
    """Opens applications based on command"""
    apps = {
        "word": "Microsoft Word",
        "excel": "Microsoft Excel",
        "powerpoint": "Microsoft PowerPoint",
        "calculator": "Calculator",
        "notes": "Notes",
        "notepad": "Notes",
        "browser": "Safari",
        "safari": "Safari",
        "chrome": "Google Chrome",
        "terminal": "Terminal",
        "system settings": "System Settings",
        "finder": "Finder",
        "discord": "Discord",
        "spotify": "Spotify",
        "vscode": "Visual Studio Code",
        "visual studio code": "Visual Studio Code",
        "zoom": "zoom.us"
    }

    for key in apps:
        if f"open {key}" in query:
            speak(f"Opening {apps[key]}")
            os.system(f"open -a '{apps[key]}'")
            return

def close_application(query):
    """Closes applications based on command"""
    apps = {
        "word": "Microsoft Word",
        "excel": "Microsoft Excel",
        "powerpoint": "Microsoft PowerPoint",
        "calculator": "Calculator",
        "notes": "Notes",
        "notepad": "Notes",
        "browser": "Safari",
        "safari": "Safari",
        "chrome": "Google Chrome",
        "terminal": "Terminal",
        "system settings": "System Settings",
        "finder": "Finder",
        "discord": "Discord",
        "spotify": "Spotify",
        "vscode": "Visual Studio Code",
        "visual studio code": "Visual Studio Code",
        "zoom": "zoom.us"
    }

    for key in apps:
        if f"close {key}" in query:
            app_name = apps[key]
            
            # Find the process ID (PID) of the application
            pid_check = os.popen(f"pgrep -f '{app_name}'").read().strip()
            
            if pid_check:
                speak(f"Closing {app_name}")
                os.system(f"pkill -f '{app_name}'")
            else:
                speak(f"{app_name} is not running.")
            return

def browsing(query):
    if 'google' in query:
        speak("Boss, what should I search on Google?")
        s = command()
        if s and s.lower() != "none":  # Ensure valid input
            search_url = f"https://www.google.com/search?q={s.replace(' ', '+')}"
            speak(f"Searching Google for {s}")
            webbrowser.open(search_url)
            return
        else:
            speak("Sorry, I couldn't find anything.")
            
def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our work")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
        
def set_volume(level):
    """Sets the system volume on a scale of 1 to 10."""
    if level < 1 or level > 10:
        speak("Please say a number between 1 and 10.")
        return
    
    volume_percentage = int((level / 10) * 100)
    
    os.system(f"osascript -e 'set volume output volume {volume_percentage}'")
    speak(f"Volume set to {level}")

def play_music(query):
    """Plays music on YouTube based on the command."""
    if "play some music" in query:
        random_songs = [
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "https://www.youtube.com/watch?v=3AtDnEC4zak",
            "https://www.youtube.com/watch?v=fLexgOxsZu0",
        ]
        song_url = random.choice(random_songs)
        speak("Playing some random music for you.")
        webbrowser.open(song_url)

    elif "play" in query:
        song_name = query.replace("play", "").strip()
        search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
        speak(f"Searching for {song_name} on YouTube.")
        webbrowser.open(search_url)

# ----End Of Core Functions---- #

# Keeps listening for commands in a loop
if __name__ == "__main__":
    # wishMe()
    while True:
        query = command().lower()

        if "open" in query:
            open_application(query)
        elif "close" in query:
            close_application(query)
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        if "volume" in query:
            words = query.split()  # Split the command into words
            for word in words:
                if word.isdigit():  # Checks if a word is a number
                    level = int(word)
                    set_volume(level)
                    break
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        if "play" in query:
            play_music(query)
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
