import customtkinter as ctk
import psutil
import threading
import speech_recognition as sr
import pyttsx3
import os
import time
from datetime import datetime
from local_ai import ask_local_ai
from local_memory import remember, recall
from logger import log_action
from system_info import (
    get_cpu_usage,
    get_ram_usage,
    get_available_ram,
    get_battery
)
from PIL import Image, ImageTk
import tkinter as tk
import webbrowser
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
import winshell
import pyperclip
import requests
from quote import quote
import random
import time
from pystray import Icon, MenuItem, Menu
from PIL import Image
import numexpr
from googletrans import Translator

translator = Translator()
import pytesseract
import PyPDF2
import cv2
import speedtest
import webbrowser
from spotify_control import play_song

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\JARVIS\tesseract.exe"
)
engine = pyttsx3.init()

engine.setProperty("rate", 170)


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
def change_volume(level):
    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )

    volume.SetMasterVolumeLevelScalar(level, None)
def speak(text):
    speaking_mode()

    print("JARVIS:", text)
    add_message(
        "JARVIS",
        text
    )

    engine.say(text)
    engine.runAndWait()
    idle_mode()


def listen():
    listening_mode()

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(
            source,
            timeout=None,
            phrase_time_limit=10
        )

    try:

        command = recognizer.recognize_google(audio)

        print("YOU:", command)
        add_message( "USER", command)

        return command.lower()

    except:
        return ""


def extract_text(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        print(e)

        return None


def wait_for_wake_word():

    while True:

        command = listen()

        if command == "":
            continue

        if "hey jarvis" in command or command.strip() == "jarvis":

            print("WAKE WORD DETECTED")
            show_window()

            speak("How can I help you?")

            return


def execute(command):

    # OPEN APPLICATIONS

    if "open chrome" in command:
        os.system("start chrome")

    elif "open notepad" in command:
        os.system("start notepad")

    elif "open calculator" in command:
        os.system("start calc")

    # CLOSE APPLICATIONS

    elif "close chrome" in command:
        os.system("taskkill /f /im chrome.exe")

    elif "close notepad" in command:
        os.system("taskkill /f /im notepad.exe")

    elif "close calculator" in command:
        os.system("taskkill /f /im CalculatorApp.exe")

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Window
app = ctk.CTk()
app.configure(fg_color="#1E1E1E")
app.attributes("-topmost", True)

app.title("JARVIS")

app.state("zoomed")


left_frame = ctk.CTkFrame(
    app,
    fg_color="#000000",
    width=400
)
center_frame = ctk.CTkFrame(app, fg_color="#000000")
right_frame = ctk.CTkFrame(app, fg_color="#000000")

left_frame.grid(row=0, column=0, sticky="ns", padx=20, pady=20)
center_frame.grid(row=0, column=1, sticky="n", padx=20, pady=20)
right_frame.grid(row=0, column=2, sticky="ns", padx=20, pady=20)

app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=2)
app.grid_columnconfigure(2, weight=5)
# Title
title = ctk.CTkLabel(
    center_frame,
    text="JARVIS",
    font=("Arial", 35, "bold"),
    text_color="#00FFFF"
)



title.pack(pady=(10,40))
gif_frames = []

gif = Image.open("voice_orb.gif")

try:
    while True:
        frame = gif.copy()
        frame = frame.resize((200,200))
        frame = ImageTk.PhotoImage(frame)
        gif_frames.append(frame)
        gif.seek(len(gif_frames))

except EOFError:
    pass


orb = tk.Label(
    center_frame,
    bg="#000000",
    borderwidth=0
)



orb.pack(pady=(10,40))

spectrum_label = ctk.CTkLabel(
    center_frame,
    text="",
    font=("Consolas",18),
    text_color="#00FFFF"
)

spectrum_label.pack()


def animate_gif(frame_num=0):

    frame = gif_frames[frame_num]

    orb.configure(image=frame)

    next_frame = (frame_num + 1) % len(gif_frames)

    app.after(
        50,
        animate_gif,
        next_frame
    )

orb.lift()

orb.lift()
orb_size = 100
growing = True

# Status
status_label = ctk.CTkLabel(
    center_frame,
    text="Status: Waiting for wake word...",
    font=("Consolas",15,"bold"),
    text_color="#00FFFF"
)



status_label.pack(pady=(0,15))



greeting_label = ctk.CTkLabel(
    center_frame,
    text="Good Evening, Sulalit",
    font=("Consolas",15),
    text_color="#00FFFF"
)



greeting_label.pack(pady=(0,10))


clock_label = ctk.CTkLabel(
    center_frame,
    text="",
    font=("Consolas",21,"bold"),
    text_color="#00FFFF"
)


clock_label.pack(pady=(0,20))


#MIC Indicator
mic_label = ctk.CTkLabel(
    center_frame,
    text="🎤",
    font=("Arial",30)
)



mic_label.pack(pady=(10,10))

wave_label = ctk.CTkLabel(
    center_frame,
    text="",
    font=("Consolas",24),
    text_color="#00FFFF"
)



wave_label.pack(pady=(0,20))

# Conversation Area
chat_title = ctk.CTkLabel(
    right_frame,
    text="CONVERSATION",
    font=("Consolas",18,"bold"),
    text_color="#00FFFF"
)

chat_title.pack(pady=(20,10))
conversation_box = ctk.CTkTextbox(
    right_frame,
    width=600,
    height=650,
    border_width=2,
    border_color="#00FFFF",
    fg_color="#101010",
    text_color="#00FFFF",
    font=("Consolas",14)
)

conversation_box.pack(
    pady=(0,20),
    fill="both",
    expand=True
)

camera_frame = ctk.CTkFrame(
    right_frame,
    fg_color="#101010",
    border_color="#00FFFF",
    border_width=2
)

camera_frame.pack(
    pady=(10,20),
    fill="both"
)


camera_title = ctk.CTkLabel(
    camera_frame,
    text="CAMERA",
    font=("Consolas",18,"bold"),
    text_color="#00FFFF"
)

camera_title.pack(pady=(10,5))

camera_label = tk.Label(
    camera_frame,
    bg="#101010",
    bd=0,
    highlightthickness=0
)

camera_label.pack(
    padx=10,
    pady=(5,10)
)
def add_message(sender, message):

    conversation_box.insert(
        "end",
        f"{sender}: {message}\n\n"
    )

    conversation_box.see("end")

# System Info Frame
system_title = ctk.CTkLabel(
    left_frame,
    text="SYSTEM STATUS",
    font=("Consolas",20,"bold"),
    text_color="#00FFFF"
)

system_title.pack(pady=(20,10))
system_frame = ctk.CTkFrame(
    left_frame,
    width=280,
    height=280,
    border_width=2,
    border_color="#00FFFF",
    fg_color="#0A0A0A"
)

system_frame.pack_propagate(False)

system_frame.pack(
    pady=10,
    padx=15,
    fill="x"
)

weather_title = ctk.CTkLabel(
    left_frame,
    text="WEATHER",
    font=("Consolas",20,"bold"),
    text_color="#00FFFF"
)

weather_title.pack(pady=(20,10))



weather_frame = ctk.CTkFrame(
    left_frame,
    border_width=2,
    border_color="#00FFFF",
    fg_color="#101010"
)

weather_frame.pack(pady=10)

weather_label = ctk.CTkLabel(
    weather_frame,
    text="Loading weather...",
    font=("Consolas",16),
    text_color="#00FFFF"
)

weather_label.pack(
    padx=20,
    pady=10
)

internet_title = ctk.CTkLabel(
    left_frame,
    text="NETWORK",
    font=("Consolas",20,"bold"),
    text_color="#00FFFF"
)

internet_title.pack(pady=(20,10))

internet_frame = ctk.CTkFrame(
    left_frame,
    border_width=2,
    border_color="#00E5FF",
    fg_color="#101010"
)

internet_frame.pack(pady=10)

internet_label = ctk.CTkLabel(
    internet_frame,
    text="Checking internet...",
    font=("Consolas",16),
    text_color="#00FFFF"
)

internet_label.pack(
    padx=20,
    pady=10
)

cpu_frame = ctk.CTkFrame(
    system_frame,
    fg_color="#101010",
    border_width=2,
    border_color="#00FFFF"
)

cpu_frame.pack(fill="x", padx=20, pady=10)


cpu_label = ctk.CTkLabel(
    cpu_frame,
    text="CPU: 0%",
    font=("Consolas",14),
    text_color="#00FFFF"
)

cpu_label.pack(pady=(10,5))

cpu_bar = ctk.CTkProgressBar(
    cpu_frame,
    width=100,
    height=18,
    corner_radius=10,
    progress_color="#00FFFF"
)

cpu_bar.set(0)
cpu_bar.pack(pady=(0,10))



ram_frame = ctk.CTkFrame(
    system_frame,
    fg_color="#101010",
    border_width=2,
    border_color="#00FFFF"
)

ram_frame.pack(fill="x", padx=20, pady=10)

ram_label = ctk.CTkLabel(
    ram_frame,
    text="RAM: 0%",
    font=("Consolas",14),
    text_color="#00FFFF"
)

ram_label.pack(pady=(10,5))

ram_bar = ctk.CTkProgressBar(
    ram_frame,
    width=100,
    progress_color="#00FFFF"
)

ram_bar.pack(pady=(0,10))




battery_frame = ctk.CTkFrame(
    system_frame,
    fg_color="#101010",
    border_width=2,
    border_color="#00FFFF"
)

battery_frame.pack(fill="x", padx=20, pady=10)

battery_label = ctk.CTkLabel(
    battery_frame,
    text="Battery: 0%",
    font=("Consolas",14),
    text_color="#00FFFF"
)

battery_label.pack(pady=(10,5))
battery_bar = ctk.CTkProgressBar(
    battery_frame,
    width=100,
    height=18,
    corner_radius=10,
    progress_color="#00FFFF"
)

battery_bar.set(0)
battery_bar.pack(pady=(0,10))


def set_status(text):

    status_label.configure(
        text=f"Status: {text}"
    )
def listening_mode():

    set_status("Listening...")

    mic_label.configure(text="🎤")

    



def thinking_mode():

    set_status("Thinking...")

    mic_label.configure(text="🤔")

    



def speaking_mode():

    set_status("Speaking...")

    mic_label.configure(text="🔊")

    



def idle_mode():

    set_status("Sleeping...")

    mic_label.configure(text="💤")

    



def animate_wave():

    patterns = [
        "▁▂▃▄▅▆▇█",
        "▂▄▆█▆▄▂",
        "▁▃▆█▇▅▂",
        "▅▆█▆▅▄▂",
        "█▇▆▅▄▃▂▁",
        "▁▂▄▆█▇▅"
    ]

    index = 0

    def update():

        nonlocal index

        if mic_label.cget("text") == "🔊":

            spectrum_label.configure(
                text=patterns[index]
            )

            index = (index + 1) % len(patterns)

        else:

            spectrum_label.configure(text="")

        app.after(
            120,
            update
        )

    update()

def update_system_info():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    battery = psutil.sensors_battery()

    cpu_label.configure(
        text=f"CPU: {cpu}%"
    )
    cpu_bar.set(cpu/100)

    ram_label.configure(
        text=f"RAM: {ram}%"
    )
    ram_bar.set(ram/100)

    
    if battery:

        battery_label.configure(
            text=f"Battery: {battery.percent}%"
        )
        battery_bar.set(battery.percent/100)
        
    else:

        battery_label.configure(
            text="Battery: N/A"
        )

    app.after(
        2000,
        update_system_info
    )

def update_clock():

    current_time = datetime.now().strftime("%I:%M:%S %p")

    current_date = datetime.now().strftime("%d %B %Y")

    clock_label.configure(
        text=f"{current_time}\n{current_date}"
    )

    app.after(
        1000,
        update_clock
    )



def update_weather():

    try:

        city = "Bhubaneswar"

        url = (
            f"https://wttr.in/{city}?format=%C+%t"
        )

        weather = requests.get(url).text

        weather_label.configure(
            text=f"{city}\n{weather}"
        )

    except:

        weather_label.configure(
            text="Weather unavailable"
        )

    app.after(
        600000,
        update_weather
    )

def update_internet_speed():

    try:

        st = speedtest.Speedtest()

        download_speed = st.download() / 1_000_000

        upload_speed = st.upload() / 1_000_000

        internet_label.configure(
            text=(
                f"Download: {download_speed:.1f} Mbps\n"
                f"Upload: {upload_speed:.1f} Mbps"
            )
        )

    except:

        internet_label.configure(
            text="Internet unavailable"
        )

    app.after(
        300000,
        update_internet_speed
    )

update_system_info()
idle_mode()
animate_wave()
update_clock()
update_weather()
update_internet_speed()

def show_window():

    app.deiconify()

    app.state("zoomed")

    app.attributes("-topmost", True)
    

def hide_window():

    app.iconify()

def read_pdf(pdf_path):

    try:

        with open(pdf_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            text = ""

            for page in reader.pages:

                text += page.extract_text()

            return text

    except Exception as e:

        print(e)

        return None
def extract_text(image_path):

    image = Image.open(image_path)

    return pytesseract.image_to_string(image)

face_detector = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)
def open_camera():

    
    print("open_camera called")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("VideoCapture created")

    

    if not cap.isOpened():
        print("Camera failed")
        speak("Camera could not be opened")
        return

    print("Camera opened successfully")

    def update_frame():

        ret, frame = cap.read()

        if ret:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = cv2.resize(frame, (500, 350))

            img = Image.fromarray(frame)

            imgtk = ImageTk.PhotoImage(img)

            camera_label.imgtk = imgtk

            camera_label.configure(image=imgtk)

        camera_label.after(10, update_frame)

    update_frame()
def detect_face():

    face_detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )

    camera = cv2.VideoCapture(0)

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,255),
                2
            )

        cv2.imshow(
            "JARVIS Face Detection",
            frame
        )

        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()

def jarvis_loop():

    while True:

        wait_for_wake_word()

        while True:

            command = listen()

            if command == "":
                continue

            thinking_mode()

            speak(f"You said {command}")
            if "stop program" in command:

                    speak("Stopping program")

                    app.quit()

                    os._exit(0)

            elif "stop listening" in command:
                

                speak("Going back to sleep")

                idle_mode()

                hide_window()

                break



            elif "open camera" in command:

                    print("Before speak")

                    speak("Opening camera")

                    app.after(0, open_camera)

                    print("After app.after")


            elif "open youtube" in command:
                    speak("Opening YouTube")
                    webbrowser.open("https://youtube.com")

            elif "open gmail" in command:
                    speak("Opening Gmail")
                    webbrowser.open("https://mail.google.com")

            elif "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://google.com")

            elif "open spotify" in command:

                    speak("Opening Spotify")

                    os.system("start spotify")
            elif "open" in command:

                    app_name = command.replace("open", "").strip()

                    speak(
                    f"I am about to open {app_name}. Please say confirm."
                )

                    confirmation = listen()

                    if "confirm" in confirmation:

                            speak(f"Opening {app_name}")

                            execute(command)

                    else:

                            speak("Operation cancelled")

            elif "close" in command:

                    app_name = command.replace("close", "").strip()

                    speak(
                    f"I am about to close {app_name}. Please say confirm."
                )

                    confirmation = listen()

                    if "confirm" in confirmation:

                            speak(f"Closing {app_name}")

                            execute(command)

                    else:

                            speak("Operation cancelled")

            elif "cpu" in command:

                    cpu = get_cpu_usage()

                    speak( f"Current CPU usage is {cpu} percent")
                    continue

            elif "ram" in command:

                    ram = get_ram_usage()

                    free_ram = get_available_ram()

                    speak(f"RAM usage is {ram} percent. Available RAM is {free_ram} gigabytes")
                    continue

            elif "battery" in command:

                    battery = get_battery()

                    if battery is not None:
    
                            speak(f"Battery level is {battery} percent")
                            continue

                    else:

                            speak("No battery detected")
                            continue
            elif "time" in command:

                    current_time = datetime.now().strftime("%I:%M %p")

                    speak(f"The current time is {current_time}")
                    continue

            elif "date" in command:

                    current_date = datetime.now().strftime("%d %B %Y")

                    speak(f"Today's date is {current_date}")
                    continue

            elif "day" in command:

                    current_day = datetime.now().strftime("%A")

                    speak(f"Today is {current_day}")
                    continue
        
            elif "remember that" in command:

                    memory_text = command.replace("remember that","").strip()

                    remember("note",memory_text)

                    speak("I will remember that.")
                    continue
            elif "what do you remember" in command:

                    note = recall("note")

                    if note:

                            speak(f"You told me {note}")
                            continue

                    else:

                            speak( "I do not remember anything yet.")
                            continue

            elif "ask ai" in command:

                    speak("What would you like to know?")

                    question = listen()

                    if question == "":
                            speak("I did not hear a question")
                    else:
                            thinking_mode()

                            speak("Thinking")

                            answer = ask_local_ai(question)

                            print(answer)

                            speak(answer[:-1])

            elif "translate" in command:

                    speak("What should I translate?")

                    text = listen()

                    if text == "":

                            speak("I did not hear anything")

                    else:

                            speak("Which language?")

                            language = listen()

                            try:

                                    translated = translator.translate(
                text,
                dest=language
            )

                                    speak(translated.text)

                            except Exception:

                                    speak("Translation failed")
            elif "open youtube" in command:

                    speak("Opening YouTube")

                    webbrowser.open("https://youtube.com")


            elif "open gmail" in command:

                    speak("Opening Gmail")

                    webbrowser.open("https://mail.google.com")


            elif "open google" in command:

                    speak("Opening Google")

                    webbrowser.open("https://google.com")


            elif "search" in command:

                    query = command.replace("search", "").strip()

                    speak(f"Searching for {query}")

                    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )


            elif "take screenshot" in command:

                    filename = datetime.now().strftime(
        "screenshot_%H_%M_%S.png"
    )

                    pyautogui.screenshot(filename)

                    speak("Screenshot saved")

            elif "shutdown computer" in command:

                    speak("Shutting down computer")

                    os.system("shutdown /s /t 5")


            elif "restart computer" in command:

                    speak("Restarting computer")

                    os.system("shutdown /r /t 5")

            elif "open downloads" in command:

                    os.startfile(
        r"C:\Users\HP\Downloads"
    )


            elif "open documents" in command:

                    os.startfile(
        r"C:\Users\HP\Documents"
    )


            elif "open desktop" in command:
    
                    os.startfile(
        r"C:\Users\HP\Desktop"
    )


            elif "type for me" in command:

                    speak("What should I type")

                    text = listen()

                    pyautogui.write(
        text,
        interval=0.05
    )

                    speak("Done")

            elif "mute volume" in command:

                    change_volume(0)

                    speak("Volume muted")


            elif "maximum volume" in command:

                    change_volume(1)

                    speak("Volume set to maximum")


            elif "half volume" in command:

                    change_volume(0.5)

                    speak("Volume set to fifty percent")

            elif "increase brightness" in command:

                    sbc.set_brightness("+20")

                    speak("Brightness increased")


            elif "decrease brightness" in command:

                    sbc.set_brightness("-20")

                    speak("Brightness decreased")


            elif "maximum brightness" in command:

                    sbc.set_brightness(100)

                    speak("Brightness set to maximum")

            elif "lock computer" in command:

                    speak("Locking computer")

                    os.system(
        "rundll32.exe user32.dll,LockWorkStation"
    )

            elif "empty recycle bin" in command:

                    winshell.recycle_bin().empty(
                    confirm=False,
                    show_progress=False,
                    sound=True
    )

                    speak("Recycle bin emptied")

            elif "read clipboard" in command:

                    text = pyperclip.paste()

                    if text:

                            speak(text)

                    else:

                            speak("Clipboard is empty")

            
            elif "copy this" in command:

                    speak("What should I copy")

                    text = listen()

                    pyperclip.copy(text)

                    speak("Copied successfully")
            elif "my ip address" in command:

                    ip = requests.get(
        "https://api.ipify.org"
    ).text

                    speak(
        f"Your IP address is {ip}"
    )


            elif "motivate me" in command:

                    q = quote()

                    speak(q)
            elif "random number" in command:

                    number = random.randint(1,100)

                    speak(
        f"Your random number is {number}"
    )

            elif "flip a coin" in command:

                    result = random.choice(
        ["Heads","Tails"]
    )

                    speak(result)

            elif "roll a dice" in command:

                    result = random.randint(1,6)

                    speak(
        f"You got {result}"
    )


            elif "start timer" in command:

                    speak(
        "For how many seconds"
    )

                    seconds = listen()

                    try:

                            seconds = int(seconds)

                            speak(
            "Timer started"
        )

                            time.sleep(seconds)

                            speak(
            "Time is up"
        )

                    except:

                            speak(
            "Invalid number"
        )

            elif "system uptime" in command:

                    boot = datetime.fromtimestamp(
        psutil.boot_time()
    )

                    speak(
        f"The computer started at {boot.strftime('%I:%M %p')}"
    )
            elif "who are you" in command:

                    speak(
        "I am Jarvis, your personal AI assistant."
    )

            elif "exit jarvis" in command:
                    speak("Goodbye")
                    app.destroy()
                    os._exit(0)

            elif "create note" in command:

                    speak("What should I write?")

                    note = listen()

                    with open("notes.txt", "a") as f:

                            f.write(note + "\n")

                            speak("Note saved")


            elif "read notes" in command:

                     try:

                            with open("notes.txt", "r") as f:

                                    notes = f.read()

                                    speak(notes)

                     except:

                            speak("No notes found")

            elif "calculate" in command:

                    expression = command.replace("calculate", "").strip()

                    expression = expression.replace("plus", "+")
                    expression = expression.replace("minus", "-")
                    expression = expression.replace("times", "*")
                    expression = expression.replace("multiplied by", "*")
                    expression = expression.replace("divided by", "/")

                    try:

                            result = numexpr.evaluate(expression)

                            speak(f"The answer is {result.item()}")

                    except:

                            speak("Sorry, I could not calculate that.")

            elif "read pdf" in command:

                    speak("Please enter the PDF path")

                    pdf_path = input("PDF path: ")

                    speak("Reading PDF")

                    text = read_pdf(pdf_path)

                    if text:

                            speak(text[:1000])

                    else:

                            speak("Could not read the PDF")

            elif "summarize pdf" in command:

                    speak("Please enter the PDF path")

                    pdf_path = input("PDF path: ")

                    text = read_pdf(pdf_path)

                    if text:

                            speak("Analyzing document")

                            prompt = f"""
Summarize the following PDF in short bullet points:

{text[:5000]}
"""

                            answer = ask_local_ai(prompt)

                            speak(answer)

                    else:

                            speak("Could not read the PDF")


            elif "read image" in command:

                    speak("Enter image path")

                    image_path = input("Image path: ")

                    text = extract_text(image_path)

                    speak(text[:1000])

            elif "read image" in command:

                    speak("Please enter the image path")

                    image_path = input("Image path: ")

                    text = extract_text(image_path)

                    if text:

                            speak(text[:1000])

                    else:

                            speak("Could not read the image")

            
            
            elif "close camera" in command:

                    camera_frame.pack_forget()

                    speak("Camera closed")
            elif "take photo" in command:

                    speak("Taking photo")

                    camera = cv2.VideoCapture(0)

                    ret, frame = camera.read()

                    if ret:

                            filename = datetime.now().strftime(
            "photo_%Y_%m_%d_%H_%M_%S.jpg"
        )

                            cv2.imwrite(
            filename,
            frame
        )

                            speak("Photo saved")

                    else:

                            speak("Could not take photo")

                    camera.release()

            elif "play a song" in command:

                    speak("Which song would you like?")

                    song = listen()

                    if song:

                            speak(f"Playing {song}")

                            success = play_song(song)

                            if not success:

                             speak("Spotify is not open")

            elif "send email" in command:

                    speak("Who should I send the email to?")

                    receiver = listen()

                    speak("What is the subject?")

                    subject = listen()

                    speak("What should I write?")

                    body = listen()

                    try:

                            send_email(
            receiver,
            subject,
            body
        )

                            speak("Email sent successfully")

                    except Exception as e:

                            print(e)

                            speak("Sorry, I could not send the email")
            else:
                    thinking_mode()

                    speak("Thinking")

                    try:
    
                            answer = ask_local_ai(command)

                            print(answer)

                            speak(answer[:-1])

                    except Exception as e:

                            print("AI ERROR:", e)
    
                            speak("Sorry, I encountered an error")


threading.Thread(
    target=jarvis_loop,
    daemon=True
).start()


def on_closing():

    app.iconify()

app.protocol("WM_DELETE_WINDOW", on_closing)
animate_gif()
app.mainloop()

