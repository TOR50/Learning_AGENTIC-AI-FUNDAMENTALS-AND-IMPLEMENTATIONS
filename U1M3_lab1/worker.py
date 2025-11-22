import requests
from openai import OpenAI

# Initialize OpenAI client (ensure you have set OPENAI_API_KEY environment variable)
# For this lab, we assume a mock or specific setup as per course instructions.
# If using real OpenAI, you need: openai_client = OpenAI(api_key="your_key")
# Here we'll assume a placeholder or pre-configured client for the lab environment.
try:
    openai_client = OpenAI()
except:
    print("OpenAI client not initialized. Ensure API key is set if running locally.")

def speech_to_text(audio_binary):
    # Set up Watson Speech-to-Text HTTP Api url
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + '/speech-to-text/api/v1/recognize'

    # Set up parameters for our HTTP request
    params = {
        'model': 'en-US_Multimedia',
    }

    # Send a HTTP Post request
    try:
        response = requests.post(api_url, params=params, data=audio_binary).json()
    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return "Error processing speech."

    # Parse the response to get our transcribed text
    text = 'null'
    if response.get('results'):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
    
    return text

def text_to_speech(text, voice=""):
    # Set up Watson Text-to-Speech HTTP Api url
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }

    # Send a HTTP Post request to Watson Text-to-Speech Service
    try:
        response = requests.post(api_url, headers=headers, json=json_data)
        print('text to speech response:', response)
        return response.content
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None

def openai_process_message(user_message):
    # Set the prompt for OpenAI Api
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations. Keep responses concise - 2 to 3 sentences maximum."
    
    try:
        # Call the OpenAI Api to process our prompt
        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000
        )
        print("openai response:", openai_response)
        # Parse the response to get the response message for our prompt
        response_text = openai_response.choices[0].message.content
        return response_text
    except Exception as e:
        print(f"Error in openai_process_message: {e}")
        return "I'm sorry, I couldn't process that request."