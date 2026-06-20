# REQUIREMENTS

## Python Version

Python 3.10 or above is recommended.

---

# Installation Steps

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Jarvis-ai-assistant
```

---

## Step 2: Install Required Libraries

Open Command Prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

---

# Python Libraries Used

* customtkinter
* psutil
* SpeechRecognition
* pyttsx3
* Pillow
* pyautogui
* pycaw
* comtypes
* screen-brightness-control
* winshell
* pyperclip
* requests
* pystray
* numexpr
* googletrans
* pytesseract
* PyPDF2
* opencv-python
* speedtest-cli
* spotipy
* numpy
* pyaudio

---

# External Software Requirements

## Tesseract OCR

Download and install Tesseract OCR.

Inside the code:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

## Ollama (Local AI)

Install Ollama.

Pull a model:

```bash
ollama pull llama3
```

Make sure Ollama is running before starting JARVIS.

---

## Spotify

Spotify Desktop application must be installed and logged in.

---

# Running JARVIS

Run:

```bash
python jarvis3.py
```

---

# Features Supported

* Voice Interaction
* Wake Word Detection
* Local AI Integration
* Memory System
* Weather Updates
* Network Speed Monitoring
* CPU, RAM and Battery Monitoring
* PDF Reading and Summarization
* OCR Image Text Extraction
* Camera Integration
* Face Detection
* Screenshot Capture
* Clipboard Operations
* Volume and Brightness Control
* Spotify Music Control
* Translation
* Mathematical Calculations
* Notes System
* File and Folder Navigation

---

# Operating System

Windows 10 or Windows 11 is recommended.

---

# Permissions Required

* Microphone Access
* Webcam Access
* Internet Connection

---

# Author

Sulalit

Project: JARVIS AI Assistant
