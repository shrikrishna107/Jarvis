import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from google import genai
from pydub import AudioSegment

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "36658f4c166d490bbfc9cddf112377e0"
FINE_TUNE_PROMPT = """
You are Jarvis, a fast and concise virtual assistant. Always give short, polite answers.
"""

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text, speed=1.5):  # speed >1 for faster audio
    tts = gTTS(text)
    tts.save("temp.mp3")

    # Speed up audio
    audio = AudioSegment.from_file("temp.mp3")
    audio = audio.speedup(playback_speed=speed)
    audio.export("temp_fast.mp3", format="mp3")

    # Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load("temp_fast.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    os.remove("temp_fast.mp3")

def aiProcess(command):
    # ✅ initialize with API key
    client = genai.Client(api_key="AIzaSyDtUJ5FindZad_r9KlIhIgGtqmYtYhpJfg")

    # ✅ generate text from Gemini
    response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        "You are Jarvis, a fast AI assistant. Be polite and keep your replies concise, but don't talk rude. And you're not supposed to read out the symboles like * or any other",  # system instructions
        command  # the user query
    ]
)

    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open chat" in c.lower():
        webbrowser.open("https://chatgpt.com/?model=auto")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    if("sleep" in command.lower()):
                        speak("Sure. See you soon")
                        break
                    else:
                        processCommand(command)

        except Exception as e:
            print("Aatein???; {0}".format(e))