import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData
stop_event=threading.Event()
def wait_for_enter():
    input("Press enter to stop recording")
    stop_event.set()
def record_until_enter():
    p=pyaudio.PyAudio()
    format=pyaudio.paInt16
    channels=1
    rate=16000
    frames_per_buffer=1024
    stream=p.open(format=format,channels=channels,rate=rate,input=True,frames_per_buffer=frames_per_buffer)
    frames=[]
    threading.Thread(target=wait_for_enter,daemon=True).start()
    while not stop_event.is_set():
        try:
            data=stream.read(frames_per_buffer)
            frames.append(data)
        except Exception as e:
            print("Error in reading stream:",e)
            break
    stream.stop_stream()
    stream.close()
    sample_width=p.get_sample_size(format)
    p.terminate()
    audio_data=b''.join(frames)
    return audio_data,rate,sample_width
def save_audio(data,rate,width,filename="audio.wav"):
    with wave.open(filename,"wb")as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"saved:{filename}")
def transcribe_audio(data,rate,width,filename="transcription.txt"):
    r=sr.Recognizer()
    audio=AudioData(data,rate,width)
    try:
        text=r.recognize_google(audio)
    except sr.UnknownValueError:
        text="Could not understand the audio"
    except sr.RequestError as e:
        text=f"API Eror:{e}"
    print("Transcription:",text)
    with open(filename,"w") as f:
        f.write(text)
    print(f"Saved:{filename}")
def main():
    print("Start speaking. Press Enter to stop recording")
    audio_data,rate,width=record_until_enter()
    save_audio(audio_data,rate,width)
    transcribe_audio(audio_data,rate,width)
if __name__=="__main__":
    main()