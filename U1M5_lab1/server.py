import logging
import os
from flask import Flask, render_template, request, jsonify
from worker import process_document, process_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process-document', methods=['POST'])
def process_document_route():
    if 'file' not in request.files:
        return jsonify({"botResponse": "No file uploaded."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"botResponse": "No file selected."}), 400

    if file:
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)
        
        try:
            process_document(file_path)
            return jsonify({"botResponse": "Document processed successfully. You can now ask questions."})
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return jsonify({"botResponse": "Error processing document."}), 500

@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json.get('userMessage')
    if not user_message:
        return jsonify({"botResponse": "Please enter a message."}), 400

    try:
        response = process_prompt(user_message)
        return jsonify({"botResponse": response})
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({"botResponse": "I'm sorry, I couldn't process your request."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
