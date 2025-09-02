import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_text(topic):
    prompt = f"Explain the topic '{topic}' in a fun, simple comic-book style suitable for students."
    print("✨ Generating explanation using Hugging Face...")

    # 1. Try Hugging Face
    hf_response = try_huggingface(prompt)
    if hf_response:
        return hf_response

    # 2. Fallback to Together.ai
    print("⚠️ Hugging Face failed. Trying Together.ai...")
    tg_response = try_together(prompt)
    if tg_response:
        return tg_response

    # 3. Final fallback message
    return "⚠️ Sorry! Could not fetch explanation due to an API error or invalid credentials."

def try_huggingface(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 500
            }
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            print(f"❌ Hugging Face Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("Exception during Hugging Face call:", e)
        return None

def try_together(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"❌ Together.ai Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("Exception during Together.ai call:", e)
        return None
