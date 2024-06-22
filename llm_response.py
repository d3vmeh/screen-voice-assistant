import requests
import os
import requests
import simpleaudio

api_key = os.getenv("OPENAI_API_KEY")
def get_llm_response(question):
    #encoded_image = encode_image(path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Answer this question with up to three sentences: {question}"},
        ]
    }

    payload = {
        "model": "gpt-4o",
        "temperature": 0.5,
        "messages": [message],
        "max_tokens": 800
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def create_audio_file(input_text,path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "tts-1",
        "voice": "alloy",
        "input": input_text,
        "response_format": "wav"
    }

    response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=payload)
    if response.status_code == 200:
        with open(path, "wb") as audio_file:
            audio_file.write(response.content)
    else:
        print(f"Failed to generate speech: {response.status_code} - {response.text}")

def play_audio(path):
    wave_obj = simpleaudio.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()