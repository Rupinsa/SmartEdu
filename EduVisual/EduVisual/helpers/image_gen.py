import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def generate_image(prompt, output_path="assets/comic_panel.png"):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {"inputs": prompt}
    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        print(f"❌ Image generation failed: {response.status_code}")
        return None
