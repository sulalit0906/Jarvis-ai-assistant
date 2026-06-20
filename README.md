# JARVIS AI Assistant

A voice-controlled personal AI assistant built with Python and CustomTkinter. JARVIS provides voice interaction, system monitoring, AI-powered responses, OCR capabilities, PDF summarization, Spotify control, and many productivity features through a futuristic desktop interface.

---

## Features

### Voice Interaction

* Wake word detection ("Hey Jarvis")
* Speech recognition
* Text-to-speech responses
* Multiple assistant states (Listening, Thinking, Speaking, Sleeping)

### System Monitoring

* CPU usage monitoring
* RAM usage monitoring
* Battery status monitoring
* Digital clock and date display

### Internet Utilities

* Weather updates
* Internet speed monitoring
* IP address retrieval

### Application Control

* Open and close applications
* Browser control
* Folder access commands
* System shutdown and restart

### Productivity Features

* Screenshot capture
* Clipboard operations
* Notes creation and reading
* Calculator
* Timer
* Random number generator
* Coin flip and dice roll

### AI Capabilities

* Local AI integration
* Memory system
* Question answering
* PDF summarization

### OCR and File Processing

* Image text extraction using Tesseract OCR
* PDF reading
* PDF summarization

### Multimedia Features

* Spotify song playback
* Camera support
* Photo capture
* Face detection (under development)

### System Controls

* Volume control
* Brightness adjustment
* Lock computer
* Empty recycle bin

### Translation

* Multi-language translation support

---

## Technologies Used

* Python
* CustomTkinter
* OpenCV
* SpeechRecognition
* pyttsx3
* Pillow
* PyAutoGUI
* PyPDF2
* pytesseract
* Google Translate
* psutil
* speedtest-cli
* pycaw
* screen-brightness-control
* Spotify API
* Local AI Model

---

## Project Structure

```text
JARVIS/
│
├── jarvis3.py
├── local_ai.py
├── local_memory.py
├── logger.py
├── system_info.py
├── spotify_control.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_LOG.md
├── AI_USAGE_REPORT.md
├── voice_orb.gif
├── haarcascade_frontalface_default.xml
└── Screenshots/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/sulalit0906/Jarvis-ai-assistant.git
```

Move into the project folder:

```bash
cd Jarvis-ai-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the assistant:

```bash
python jarvis3.py
```

---

## Future Improvements

* Face recognition
* Object detection
* Gesture control
* Home automation integration
* RAG-based knowledge system
* Agentic workflows
* Cloud deployment
* Mobile companion application

---

## Author

**Sulalit**

Created as part of the **AI Vibe Coding Challenge 2026**.

---

## License

This project is intended for educational and research purposes.

