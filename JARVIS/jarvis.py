import datetime
from email.mime import audio
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pyaudio


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Mr. stark!")

    elif hour>=12 and hour<18:
        speak("Good afternoon Mr. stark!")
    
    else:
        speak("Good evening Mr. stark!")

    speak("jarvis is on work  how can i help you")

def takeCommand():
    #it take audio as input from user and return string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query =r.recognize_google(audio,Language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        #print(e)
        print("pardon sir please say again")
        return "None"
    return query
if __name__=="__main__":
    wishMe()
    #speak("hello sir, i am jarvis")
    while True:
        query = takeCommand().lower()

        #logic for exicuting tasks based on query
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query=query.replace('wikipedia',"")
            results = wikipedia.summary(query,sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube'in query:
            webbrowser.open("youtube.com")

        elif 'open google'in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow'in query:
            webbrowser.open("stackoverflow.com")

        elif 'the time'in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'open vs code'in query:
            codepath="C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)
        
        
        
        
        
