import pyaudio
import wave

def record_voice(output_path, format = pyaudio.paInt16, rate = 16000, chunk = 1024, channels = 1, chunk_record_time = 5):
    #print("recording voice")
    frames = []

    format = format
    rate = rate
    chunk = chunk
    channels = channels

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)


    frames = []

    for i in range(0, int(rate/chunk * chunk_record_time)):
        data = stream.read(chunk, exception_on_overflow = True)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    #print("Recording saved")


def push_to_talk_start(stream, audio, frames, format = pyaudio.paInt16, rate = 16000, chunk = 1024, channels = 1):
    format = format
    rate = rate
    chunk = chunk
    channels = channels

    data = stream.read(chunk)
    frames.append(data)
    return stream, audio, rate, channels, format, frames
    
def push_to_talk_end(output_path, stream, audio, rate, channels, format, frames):
    stream.stop_stream()
    stream.close()
    
    print(len(frames), "Saving recording")
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()