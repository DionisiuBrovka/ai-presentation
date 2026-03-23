import os
from groq import Groq

def wav_to_text(filename:str) -> str:
    client = Groq()
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        temperature=0,
        language="ru",
        response_format="verbose_json",
        )
    print(transcription.text)