# Lab 6: Babel Fish (Voice Translator)

## 🎯 Objective
Build a voice-to-voice translation assistant that:
1.  **Listens**: Converts English speech to text using **Watson Speech-to-Text**.
2.  **Translates**: Translates text to Spanish using **Watsonx Mistral LLM**.
3.  **Speaks**: Converts the translation back to speech using **Watson Text-to-Speech**.

## 🛠️ Prerequisites
```bash
pip install -r requirements.txt
```

## 💻 Implementation

### 1. Worker (`worker.py`)
Handles API calls to Watson services (STT, TTS, and LLM).

### 2. Server (`server.py`)
Flask backend to expose endpoints for the frontend.

## 🚀 Running the App
```bash
python server.py
```


