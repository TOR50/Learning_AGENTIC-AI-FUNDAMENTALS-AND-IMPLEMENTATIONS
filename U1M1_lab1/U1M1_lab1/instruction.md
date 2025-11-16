# Lab 1: Image Captioning with BLIP & Gradio

## 🎯 Objective
Build an AI-powered image captioning tool using Hugging Face Transformers (BLIP model) and create a web interface with Gradio.

## 🛠️ Prerequisites
Ensure your environment is set up (see [README.md](./README.md)).
```bash
pip install -r requirements.txt
```

## 📝 Tasks

### 1. Basic Image Captioning
Create a script `image_cap.py` to generate captions for local images.

```python
import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load image
img_path = "assets/your_image.jpg" # Update with your image path
image = Image.open(img_path).convert('RGB')

# Generate caption
text = "the image of"
inputs = processor(images=image, text=text, return_tensors="pt")
outputs = model.generate(**inputs, max_length=50)
caption = processor.decode(outputs[0], skip_special_tokens=True)

print(caption)
```

### 2. Gradio Web App
Create `image_captioning_app.py` to build an interactive UI.

```python
import gradio as gr
import numpy as np
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_image(input_image: np.ndarray):
    raw_image = Image.fromarray(input_image).convert('RGB')
    inputs = processor(images=raw_image, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

iface = gr.Interface(
    fn=caption_image, 
    inputs=gr.Image(), 
    outputs="text",
    title="Image Captioning",
    description="Generate captions for images using the BLIP model."
)

iface.launch()
```

### 3. Automated URL Captioner
Create `automate_url_captioner.py` to scrape and caption images from a website.

```python
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Scrape
url = "https://en.wikipedia.org/wiki/IBM"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
img_elements = soup.find_all('img')

with open("captions.txt", "w", encoding="utf-8") as f:
    for img in img_elements:
        img_url = img.get('src')
        if not img_url or not img_url.startswith('//'): continue
        
        try:
            img_url = "https:" + img_url
            raw_image = Image.open(BytesIO(requests.get(img_url).content)).convert('RGB')
            if raw_image.size[0] * raw_image.size[1] < 200: continue # Skip tiny images
            
            inputs = processor(images=raw_image, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            f.write(f"{img_url}: {caption}\n")
            print(f"Captioned: {img_url}")
        except Exception as e:
            continue
```

## 🚀 Running the Code
Run the scripts from your terminal:
```bash
python image_cap.py
python image_captioning_app.py
python automate_url_captioner.py
```
