import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
import wikipedia
import webbrowser
import os
import subprocess
import datetime
import requests
from PyQt5.QtGui import QPixmap
import webview

class AIAssistant(QMainWindow):
    def find_files_by_extension(self, directory, extension):
        matching_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    matching_files.append(os.path.join(root, file))
        return matching_files
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Alice AI: A talking software')
        self.setGeometry(100, 100, 600, 400)

        background_label = QLabel(self)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        background_url = "https://github.com/Yash12007/Alice_AI/blob/main/BG.jpg?raw=true"  # Replace with your image URL
        self.set_background_image(background_url, background_label)

        self.layout = QVBoxLayout() # type: ignore

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        self.input_field = QLineEdit(self)
        self.layout.addWidget(self.input_field)

        self.record_button = QPushButton('Ask question', self)
        self.webAI = QPushButton('Open Alice AI - ChatBot: Large database', self)

        self.record_button.setStyleSheet('background-color: rgba(153, 0, 255, 0.7); color: white;')
        self.webAI.setStyleSheet('background-color: rgba(153, 0, 255, 0.7); color: white;')
        
        self.record_button.clicked.connect(self.start_listening)
        self.webAI.clicked.connect(self.start_webAI)

        self.layout.addWidget(self.record_button)
        self.layout.addWidget(self.webAI)

        self.central_widget.setLayout(self.layout)
        
        self.text_display.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color:white;")  # Adjust the RGBA values as needed
        self.input_field.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius:10px; border: 1px solid rgb(153, 0, 255); color: rgb(153, 0, 255);")  # Adjust the RGBA values as needed
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        directory = os.getcwd()
        self.text_display.setPlainText(f"""Status: Online
                                       
Logs:    
    Date of use: {datetime.datetime.now().date()}
    Time of use: {datetime.datetime.now().strftime('%H:%M:%S')}
    User login: {os.getlogin()}
    Current Working Directory: {os.getcwd()}
    CPU: {os.cpu_count()}
    Files/Directories: {os.listdir(directory)}\n
Powered by:
    Yash12007: A software development company.
    Website: https://yash12007.github.io/
""")
        
    def start_webAI(self):
        webview.create_window(
            "Alice AI - ChatBot",
            url='https://mediafiles.botpress.cloud/5cabeefc-cfd0-4681-84c6-b2d2b741e6f6/webchat/bot.html',
            width=400,
            height=600
        )
        webview.start()
        
    def set_background_image(self, url, label):
        ico = 'https://icons.getbootstrap.com/assets/icons/box.svg'
        response = requests.get(url)
        image_data = response.content
        ico_response = requests.get(ico)
        ico_data = ico_response.content
        pixmap = QPixmap()
        ico_pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        ico_pixmap.loadFromData(ico_data)
        self.setWindowIcon(QIcon(ico_pixmap))
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, 1920, 1080)

    def start_listening(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"User said: {query}")
            self.input_field.setText(f'Query: {query}')
            self.process_query(query)

        except sr.UnknownValueError:
            print("Could not understand audio")
            self.speak('Could not understand audio')

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            self.speak('Error in recognition of your voice.')

    def process_query(self, query):
        if 'Wikipedia' in query:
            self.speak('Searching on wikipedia...')
            self.text_display.setPlainText("Searching on wikipedia...")
            self.search_wikipedia(query.replace('Wikipedia', '').strip())

        elif 'open YouTube' in query:
            self.speak('Opening YouTube...')
            self.text_display.setPlainText("Opening YouTube...[https://www.youtube.com/]")
            webbrowser.open("https://www.youtube.com/")

        elif 'open Google' in query:
            self.speak('Opening Google...')
            self.text_display.setPlainText("Opening Google...[https://www.google.com/]")
            webbrowser.open("https://www.google.com/")

        elif 'open Stack Overflow' in query:
            self.speak('Opening stack overflow...')
            self.text_display.setPlainText("Opening Stack Overflow...[https://stackoverflow.com/]")
            webbrowser.open("https://stackoverflow.com/")

        elif 'play music' in query:
            self.speak('Finding songs in your device...')
            ext = query.replace('search', '')
            directory_to_search = f"C:\\users\\{os.getlogin()}\\"
            target_extension = '.mp3'
            result = AIAssistant.find_files_by_extension(self, directory_to_search, target_extension)
            list_songs = []
            for file_path in result:
                list_songs.append(file_path)
            self.text_display.setPlainText(f"Playing music...\n\nSongs found in your device: {list_songs}")
            if list_songs:
                self.text_display.setPlainText(f"Found {len(result)} files with the extension '{target_extension}':\n\n{list_songs}")
                os.startfile(os.path.join(f'C:\\users\\{os.getlogin()}\\Music', list_songs[0]))
            else:
                self.text_display.setPlainText("No music found in the 'Music' folder.")

        elif 'what time' in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.text_display.setPlainText(f"Current time is {current_time}")
            self.speak(f"Current time is {current_time}")

        elif 'open code' in query:
            self.speak("Opening Visual Studio Code.")
            subprocess.Popen('code .', shell=True)
            self.text_display.setPlainText("Opening Visual Studio Code.")

        elif 'open spotify' in query:
            self.text_display.setPlainText('Opening spotify...[https://www.spotify.com/]')
            self.speak('Opening spotify...')
            webbrowser.open('https://www.spotify.com/')
        
        elif '.com' in query:
            self.text_display.setPlainText('Opening webpage...')
            self.speak('Opening webpage...')
            webbrowser.open(query)

        elif '.org' in query:
            self.text_display.setPlainText('Opening webpage...')
            self.speak('Opening webpage...')
            webbrowser.open(query)

        elif '.co' in query:
            self.text_display.setPlainText('Opening webpage...')
            self.speak('Opening webpage...')
            webbrowser.open(query)

        elif '.in' in query:
            self.text_display.setPlainText('Opening webpage...')
            self.speak('Opening webpage...')
            webbrowser.open(query)

        elif '.jp' in query:
            self.text_display.setPlainText('Opening webpage...')
            self.speak('Opening webpage...')
            webbrowser.open(query)

        elif 'exit' in query:
            self.text_display.setPlainText("Have a good day!")
            self.speak("Have a good day!")
            exit()

        elif 'open cmd' in query:
            self.text_display.setPlainText(f'Opening CMD...')
            self.speak('Opening CMD...')
            subprocess.run('cmd', shell=True)
        
        elif 'show app' in query:
            self.text_display.setPlainText('Showing all Applications in your devices.')
            self.speak('Showing all applications in your device, It will take some time to show.')
            result = subprocess.run(['powershell', 'Get-WmiObject -Class Win32_Product | Select-Object Name'], capture_output=True, text=True)
            self.text_display.setPlainText(f'All Applications:\n\n{result.stdout}')

        elif 'search' in query:
            self.speak('Searching in your device...')
            ext = query.replace('search ', '')
            directory_to_search = f"C:\\users\\{os.getlogin()}\\"
            target_extension = f'.{ext}'
            result = AIAssistant.find_files_by_extension(self, directory_to_search, target_extension)
            list_search = []
            for file_path in result:
                list_search.append(file_path)
            self.text_display.setPlainText(f'Search results:\n\n{list_search}')

        else:
            self.speak('Could not understand your query') 

    def search_wikipedia(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            self.text_display.setPlainText(result)
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.text_display.setPlainText(f"Ambiguous search term. Please be more specific. {e}")
            self.speak(f"Ambiguous search term. Please be more specific. {e}")
        except wikipedia.exceptions.PageError as e:
            self.text_display.setPlainText(f"No results found. {e}")
            self.speak(f"No results found. {e}")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == '__main__':
    app = QApplication([])
    window = AIAssistant()
    window.show()
    window.speak('Hello, My name is Alice, Your personal talking AI assistant. Please tell me how may I help you?')
    app.exec_()
    
