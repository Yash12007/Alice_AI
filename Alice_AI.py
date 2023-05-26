import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import openai
from tkinter.ttk import Progressbar
from tkinter import *

def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices= engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio) 
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("My name is Alice AI. Make sure you are connected to internet and Please tell me how may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        speak("Recognizing...")    
        query = r.recognize_google(audio, language='en-in ')
        print(f"User said: {query}\n")
        speak("Searching...")
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please")  
        return "None"
    return query

def search(chatprompt):
    r = open("Data.txt", "r")
    c=str(r.read())
    r.close()
    openai.api_key = c
    model_engine = "text-davinci-003"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=chatprompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = completion.choices[0].text
    print(response)
    speak(response)

def work():
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching on Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'none' in query:
            work()
        
        elif 'what is your name' in query:
            print("My name is Alice AI")
            speak("My name is Alice AI")
        
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("https://stackoverflow.com/")   

        elif 'open whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com/")

        elif 'open facebook' in query:
            webbrowser.open("https://www.facebook.com/")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com/")

        elif 'open snapchat' in query:
            webbrowser.open("https://web.snapchat.com/")

        elif 'open spotify' in query:
            webbrowser.open("https://open.spotify.com/")

        elif 'music' in query:
            webbrowser.open("https://open.spotify.com/")

        elif 'blogger' in query:
            webbrowser.open("https://www.blogger.com/")
        
        elif 'song' in query:
            webbrowser.open("https://open.spotify.com/")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'exit' in query:
            exit()
        
        else:
            search(chatprompt=query)

def pro():
    p1['value']+=1
    l1.config(text=f"{int(p1['value'])}%")
    if p1["value"] == 101:
        root.quit()
        wishMe()
        work()
    else:
        p1.after(10, pro)

def submit():
    f = open("Data.txt", "w")
    f.write(str(e1.get()))
    f.close()
    pro()

def create():
    webbrowser.open("https://platform.openai.com/account/api-keys")

if __name__=='__main__':
    root = Tk()
    root.geometry("400x400")
    root.title("Alice AI")
    root.config(background="black")
    t1 = Label(root, text="Welcome to Alice AI", fg="cyan", bg="black", font=("calibre", 19))
    t1.pack()
    p1=Progressbar(root, length=300, orient=HORIZONTAL)
    p1.pack()
    l1 = Label(root, text="0%", fg="cyan", bg="black")
    l1.pack()
    Label(root, text="To close the Application Say 'Exit'", fg="cyan", bg="black", font=("Arial", 12, "bold")).pack()
    if (os.path.exists("Data.txt") == True):
            pro()
    elif (os.path.exists("Data.txt") == False):
        l2 = Label(root, text="Enter your OpenAI API_KEY", fg="cyan", bg="black", font=("Arial", 12, "bold")).pack()
        e1 = Entry(root)
        e1.pack()
        b2 = Button(root, text="Create API_KEY", fg="cyan", bg="black", font=("Arial", 12, "bold"), command=create).pack(side=RIGHT, anchor="se")
        b1 = Button(root, text="Submit", fg="cyan", bg="black", font=("Arial", 12, "bold"), command=submit).pack(side=RIGHT, anchor="se")
    root.mainloop()

