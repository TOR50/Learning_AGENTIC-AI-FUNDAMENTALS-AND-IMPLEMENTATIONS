import requests
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

# Define the credentials 
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
}

PROJECT_ID = "skills-network"

# Specify model_id that will be used for inferencing
model_id = "mistralai/mistral-medium-2505"

# Define the model parameters
parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
try:
    model = Model(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=PROJECT_ID
    )
except Exception as e:
    print(f"Error initializing Watsonx Model: {e}")
    model = None

def speech_to_text(audio_binary):
    # Set up Watson Speech-to-Text HTTP Api url
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    
    # Set up parameters for our HTTP request
    params = {
        'model': 'en-US_Multimedia',
    }
    
    # Send a HTTP Post request
    try:
        response = requests.post(api_url, params=params, data=audio_binary).json()
        
        # Parse the response to get our transcribed text
        text = 'null'
        if response.get('results'):
            print('Speech-to-Text response:', response)
            text = response.get('results').pop().get('alternatives').pop().get('transcript')
            print('recognised text: ', text)
            return text
    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return "Error processing speech"
    return text

def text_to_speech(text, voice=""):
    # Set up Watson Text-to-Speech HTTP Api url
    base_url = 'https://sn-watson-tts.labs.skills.network'
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
        print('Text-to-Speech response:', response)
        return response.content
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None

def watsonx_process_message(user_message):
    if not model:
        return "Model not initialized."

    # Set the prompt for Watsonx API - using a strict translation instruction
    prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.
    English: {user_message}
    Spanish:
    """
    try:
        response_text = model.generate_text(prompt=prompt)
        print("wastonx response:", response_text)
        return response_text.strip()
    except Exception as e:
        print(f"Error in watsonx_process_message: {e}")
        return "Error processing message"
