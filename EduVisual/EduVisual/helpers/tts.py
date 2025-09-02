from gtts import gTTS

def text_to_speech(text, output_path="output/explanation.mp3"):
    tts = gTTS(text)
    tts.save(output_path)
    print("✅ Voice narration saved.")
