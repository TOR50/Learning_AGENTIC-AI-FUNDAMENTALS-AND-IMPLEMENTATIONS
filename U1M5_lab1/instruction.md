# Lab 5 Instructions: Chatbot for Your Data

## 1. Setup Environment
Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Document Processing (`worker.py`)
This script handles:
*   **Initialization**: Sets up WatsonX Llama 3 and HuggingFace Embeddings.
*   **Document Loading**: Loads PDF using `PyPDFLoader`.
*   **Splitting**: Splits text into chunks using `RecursiveCharacterTextSplitter`.
*   **Vector Store**: Creates a `Chroma` database for retrieval.
*   **Retrieval Chain**: Uses `RetrievalQA` to answer questions based on the document.

## 3. Server (`server.py`)
Flask server with endpoints:
*   `/process-document`: Uploads and processes the PDF.
*   `/process-message`: Handles user questions and returns answers from the LLM.

## 4. Interface (`templates/index.html`)
A simple web interface to:
1.  Upload a PDF document.
2.  Chat with the bot about the document's content.

## 5. Running the App
```bash
python server.py
```
Access the app at `http://localhost:8000`.
