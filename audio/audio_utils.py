import streamlit as st
import sounddevice as sd
import soundfile as sf
import tempfile
import os

def save_uploaded_audio(uploaded_file) -> str:
    """Save uploaded audio to temp folder"""
    save_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def record_audio(duration=10, fs=44100) -> str:
    """Record live audio using microphone"""
    st.info(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    temp_file = os.path.join(tempfile.gettempdir(), "live_record.wav")
    sf.write(temp_file, audio_data, fs)
    return temp_file
