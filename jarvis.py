# imported 
import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import sys
import psutil
import pyautogui
import geocoder
import webbrowser
import pywhatkit as kit
import smtplib
import requests 
import pyjokes
from requests import get
from PyQt5 import QtWidgets , QtCore,QtGui
from PyQt5.QtCore import QTime, QDate, Qt,QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie,QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi  import Ui_JarvisUi
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def spext(audio):
    engine.say(audio)
    engine.runAndWait()

def loco():
    try:
        response = requests.get("https://ipinfo.io/")
        data = response.json()
        city = data.get("city")
        country = data.get("country")
        location = f"You are currently in {city}, {country}"
        spext(location)
    except Exception:
        spext("Sorry sir, due to internet issues I was unable to determine our location")
        

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        spext("Good Morning sir")
    elif hour > 12 and hour <= 18:
        spext("Good Afternoon sir")
    else:
        spext("Good Evening sir")
    spext("How may I help you today?")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    def run(self):
        self.tasks()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                return query.lower()
            except:
                spext("Could not understand")
                return "None"

    def tasks(self):
        wish()
        while True:
            self.query = self.takecommand()
            if self.query == "None":
                continue

            elif "open ms" in self.query:
                os.startfile("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")

            elif "open command" in self.query:
                os.system("start cmd")

            elif "search" in self.query:
                spext("Searching Wikipedia...")
                try:
                    query = self.query.replace("wiki", "")
                    results = wikipedia.summary(query, sentences=2)
                    spext("According to Wikipedia")
                    spext(results)
                except:
                    spext("Couldn't find anything on Wikipedia")

            elif "how much battery left" in self.query:
                battery = psutil.sensors_battery()
                per = battery.percent
                if per <= 30:
                    spext(f"Sir, only {per} percent remaining!")
                elif per >= 60:
                    spext("We have sufficient power sir!")

            elif "decrease volume" in self.query:
                pyautogui.press("volumedown")

            elif "where are we" in self.query:
                spext("Let me check sir")
                loco()

            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                spext(joke)

            elif "shutdown the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "open youtube" in self.query:
                webbrowser.open("https://www.youtube.com")

            elif "open google" in self.query:
                spext("Sir, what should I search on Google?")
                cm = self.takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")

            elif "play on youtube" in self.query:
                spext("Sir, what should I play?")
                sg = self.takecommand().lower()
                kit.playonyt(sg)

            elif "send mail" in self.query:
                try:
                    spext("What should I say?")
                    content = self.takecommand().lower()
                    to = "gsrpk.sg@gmail.com"
                    sendEmail(to, content)
                    spext("Email successfully sent sir")
                except Exception as e:
                    print(e)
                    spext("Sorry sir, I was not able to send the mail")

            elif "how are you" in self.query:
                spext("I am fine sir. How about you?")

            elif "exit" in self.query:
                spext("Ok sir. Do you want something else?")
                break

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('gsraj0301@gmail.com', 'fvos ssfv ubdo mfph')
    server.sendmail('gsraj0301@gmail.com', to, content)
    server.close()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.starttask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def starttask(self):
        self.ui.movie = QtGui.QMovie("../../Pictures/7c61406369bffe8bc8d339d83ab1dd81.gif")
        self.ui.label.setMovie(self.ui.movie)    
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../Pictures/jarvis ui.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie = QtGui.QMovie("../../Pictures/00545cb7179c504433d4c8f5e845f286.gif")
        self.ui.label_3.setMovie(self.ui.movie)    
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)
        startExecution.start()

    def showtime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.ui.textBrowser.setText(current_time.toString('hh:mm:ss'))
        self.ui.textBrowser_2.setText(current_date.toString(Qt.ISODate))

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())

