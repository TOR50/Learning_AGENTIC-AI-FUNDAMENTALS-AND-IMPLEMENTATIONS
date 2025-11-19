from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

model_name = "facebook/blenderbot-400M-distill"

# Load model and tokenizer
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
print("Model loaded!")

conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json.get("msg")
    
    global conversation_history
    history_string = "\n".join(conversation_history)

    inputs = tokenizer.encode_plus(history_string, user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    conversation_history.append(user_input)
    conversation_history.append(response)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
