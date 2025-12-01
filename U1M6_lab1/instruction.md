# Lab 6 Instructions: Babel Fish with LLM STT TTS

## 1. Setup Environment
Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Worker (`worker.py`)
This script handles the core logic:
*   **Watsonx LLM**: Uses `mistralai/mistral-medium-2505` for translation.
*   **Speech-to-Text**: Uses Watson STT API to transcribe audio.
*   **Text-to-Speech**: Uses Watson TTS API to synthesize speech.

## 3. Server (`server.py`)
Flask server with endpoints:
*   `/speech-to-text`: Receives audio, returns transcribed text.
*   `/process-message`: Receives text, translates it to Spanish, and returns audio.

## 4. Running the App
```bash
python server.py
```
Access the app at `http://localhost:8000`.
