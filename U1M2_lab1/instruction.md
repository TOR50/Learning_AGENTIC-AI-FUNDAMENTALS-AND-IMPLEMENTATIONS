# Lab 2 Instructions: Simple Chatbot with Open Source LLMs

## 1. Setup Environment
Install dependencies:
```bash
pip install transformers==4.30.2 torch flask flask-cors
```

## 2. Terminal Chatbot (`chatbot.py`)
Create a script to chat via terminal using `facebook/blenderbot-400M-distill`.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = []

while True:
    history_string = "\n".join(conversation_history)
    input_text = input("> ")
    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(response)
    conversation_history.append(input_text)
    conversation_history.append(response)
```

## 3. Web Application (`app.py`)
Create a Flask app to serve a web interface.

```python
from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
model_name = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json.get("msg")
    history_string = "\n".join(conversation_history)
    inputs = tokenizer.encode_plus(history_string, user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    conversation_history.append(user_input)
    conversation_history.append(response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
```

## 4. Web Interface (`templates/index.html`)
Simple HTML/JS for the chat UI.

```html
<!DOCTYPE html>
<html>
<body>
    <div id="chat-box"></div>
    <input type="text" id="user-input">
    <button onclick="sendMessage()">Send</button>
    <script>
        async function sendMessage() {
            let msg = document.getElementById("user-input").value;
            let response = await fetch("/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ msg: msg })
            });
            let data = await response.json();
            document.getElementById("chat-box").innerHTML += `<div>You: ${msg}</div><div>AI: ${data.response}</div>`;
        }
    </script>
</body>
</html>
```

## 5. Chatbot API (`app2.py`)
Create a standalone API endpoint.

```python
from flask import Flask, request
from flask_cors import CORS
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
CORS(app)

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = []

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    data = json.loads(request.get_data(as_text=True))
    input_text = data['prompt']
    history = "\n".join(conversation_history)
    inputs = tokenizer.encode_plus(history, input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=60)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    conversation_history.append(input_text)
    conversation_history.append(response)
    return response

if __name__ == '__main__':
    app.run()
```
