# Lab 4 Instructions: Business AI Meeting Companion

## 1. Setup Environment
Install dependencies:
```bash
pip install -r requirements.txt
sudo apt update && sudo apt install ffmpeg -y
```

## 2. Simple Speech-to-Text (`simple_speech2text.py`)
Download an audio file and transcribe it using OpenAI Whisper.
```python
import requests
from transformers import pipeline

# Download audio
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX04C6EN/Testing%20speech%20to%20text.mp3"
with open("downloaded_audio.mp3", "wb") as f:
    f.write(requests.get(url).content)

# Transcribe
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)
print(pipe("downloaded_audio.mp3", batch_size=8)["text"])
```

## 3. Audio Transcription App (`speech2text_app.py`)
Gradio interface for transcribing uploaded audio.
```python
import gradio as gr
from transformers import pipeline

def transcript_audio(audio_file):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)
    return pipe(audio_file, batch_size=8)["text"]

gr.Interface(fn=transcript_audio, inputs=gr.Audio(sources="upload", type="filepath"), outputs=gr.Textbox(), title="Audio Transcription App").launch(server_name="0.0.0.0", server_port=7860)
```

## 4. Simple LLM Generation (`simple_llm.py`)
Generate text using IBM WatsonX Llama 3.
```python
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

credentials = {"url": "https://us-south.ml.cloud.ibm.com"}
params = {GenParams.MAX_NEW_TOKENS: 700, GenParams.TEMPERATURE: 0.1}
model = Model(model_id='meta-llama/llama-3-2-11b-vision-instruct', credentials=credentials, params=params, project_id="skills-network")
llm = WatsonxLLM(model)
print(llm("How to read a book effectively?"))
```

## 5. Meeting Companion App (`speech_analyzer.py`)
Combine STT and LLM to transcribe and summarize audio.
```python
import gradio as gr
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# LLM Setup
credentials = {"url": "https://us-south.ml.cloud.ibm.com"}
params = {GenParams.MAX_NEW_TOKENS: 700, GenParams.TEMPERATURE: 0.1}
model = Model(model_id='meta-llama/llama-3-2-11b-vision-instruct', credentials=credentials, params=params, project_id="skills-network")
llm = WatsonxLLM(model)

# Prompt
template = """List the key points with details from the context:\n[INST] The context : {context} [/INST]"""
chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["context"], template=template))

# STT & Process
def process_audio(audio_file):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny.en", chunk_length_s=30)
    transcript = pipe(audio_file, batch_size=8)["text"]
    return chain.run(transcript)

# Interface
gr.Interface(fn=process_audio, inputs=gr.Audio(sources="upload", type="filepath"), outputs=gr.Textbox(), title="Speech Analyzer").launch(server_name="0.0.0.0", server_port=7860)
```
