# Import necessary packages
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
import gradio as gr

# Set credentials to use the model
credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                  )

# Model and project settings
model_id = "meta-llama/llama-3-2-11b-vision-instruct"  # Directly specifying the LLAMA3 model
project_id = "skills-network"  # Specifying project_id as provided

params = TextChatParameters(
    temperature=0.1,
    max_tokens=256
)

# Initialize the model
model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=params
)

# Function to generate a response from the model
def generate_response(prompt_txt):
    messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_txt
            },
        ]
    }
]   
    generated_response = model.chat(messages=messages)
    generated_text = generated_response['choices'][0]['message']['content']
    return generated_text

# Create Gradio interface
chat_application = gr.Interface(
    fn=generate_response,
    flagging_mode="never",
    inputs=gr.Textbox(label="Input", lines=2, placeholder="Type your question here..."),
    outputs=gr.Textbox(label="Output"),
    title="Watsonx.ai Chatbot",
    description="Ask any question and the chatbot will try to answer."
)

# Launch the app
if __name__ == "__main__":
    chat_application.launch(server_name="0.0.0.0", server_port= 7860)