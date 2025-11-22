# Lab 3 Instructions: Voice Assistant with OpenAI & Watson

## 1. Setup Project
Clone the starter code:
```bash
git clone https://github.com/ibm-developer-skills-network/bkrva-chatapp-with-voice-and-openai-outline.git
mv bkrva-chatapp-with-voice-and-openai-outline chatapp-with-voice-and-openai-outline
cd chatapp-with-voice-and-openai-outline
```

## 2. Run Application (Docker)
Build and run the container:
```bash
docker build . -t voice-chatapp-powered-by-openai
docker run -p 8000:8000 voice-chatapp-powered-by-openai
```

## 3. Speech-to-Text (`worker.py`)
Implement `speech_to_text` to convert audio to text using Watson:
```python
def speech_to_text(audio_binary):
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    params = {'model': 'en-US_Multimedia'}
    
    response = requests.post(api_url, params=params, data=audio_binary).json()
    
    text = 'null'
    while bool(response.get('results')):
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        return text
    return text
```

## 4. Text-to-Speech (`worker.py`)
Implement `text_to_speech` to convert text to audio using Watson:
```python
def text_to_speech(text, voice=""):
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
        
    headers = {'Accept': 'audio/wav', 'Content-Type': 'application/json'}
    json_data = {'text': text}
    
    response = requests.post(api_url, headers=headers, json=json_data)
    return response.content
```

## 5. OpenAI Integration (`worker.py`)
Implement `openai_process_message` to generate responses:
```python
def openai_process_message(user_message):
    prompt = "Act like a personal assistant. Keep responses concise."
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": prompt}, 
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000
    )
    return openai_response.choices[0].message.content
```

## 6. Server Endpoints (`server.py`)
Implement the Flask routes:

**Speech to Text Route:**
```python
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return jsonify({'text': text})
```

**Process Message Route:**
```python
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage']
    voice = request.json.get('voice', '')
    
    openai_response_text = openai_process_message(user_message)
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])
    
    openai_response_speech = text_to_speech(openai_response_text, voice)
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')
    
    return jsonify({
        "openaiResponseText": openai_response_text, 
        "openaiResponseSpeech": openai_response_speech
    })
```
