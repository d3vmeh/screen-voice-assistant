from faster_whisper import WhisperModel
from PIL import ImageGrab
import keyboard
from llm_response import *
from record_voice import *
import pyaudio
import time


def get_transcription_from_audio(audio_path, model_size = "base"):
   # Run on GPU with FP16
   model = WhisperModel(model_size, device="cuda", compute_type="float16")
   segments, info = model.transcribe(audio_path, beam_size=5)

   transcription = ' '.join([segment.text for segment in segments])
   return transcription

def take_screenshot(path):
    screenshot = ImageGrab.grab()
    screenshot.save(path)



image_path = "./screenshots/screenshot.png"
recording_path = "./audio/recording.wav"
response_path = "./audio/response.wav"

count = 0
frames = []
format = pyaudio.paInt16
channels = 1
rate = 16000
chunks = 1024

while True:

    if keyboard.is_pressed('`') and count == 0:
        take_screenshot(image_path)
        print("Start recording")
        audio = pyaudio.PyAudio()
        stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunks)
        count = 1
    if keyboard.is_pressed('`') == True and count == 1:
        print("recording...")
        stream, audio, rate, channels, format, frames = push_to_talk_start(stream, audio, frames)
        count = 1
    if keyboard.is_pressed('`') == False and count == 1:
        print("stopping recording")
        push_to_talk_end(recording_path, stream, audio, rate, channels, format, frames)
        count = 0
        transcription = get_transcription_from_audio(recording_path, model_size = "tiny")
        print(transcription)

        response = get_llm_response(transcription, image_path)

        print(response["choices"][0]["message"]["content"])
        create_audio_file(response["choices"][0]["message"]["content"],response_path)
        play_audio(response_path)
        frames = []
    
    if keyboard.is_pressed('`') == False and count == 0:
        #print("not recording")
        time.sleep(0.25)
    # if keyboard.is_pressed("F7"):# and count == 0:
    #     count = 1
    #     take_screenshot(path)
    #     response = extract_text(path)
    #     response_text = response["choices"][0]["message"]["content"]
    #     print(response_text)
    #     create_audio_file(response_text,audio_path)
    #     play_audio(audio_path)
    #     print("played audio")
    
    #time.sleep(0.1)
    #count = 0
