from silero_tts.silero_tts import SileroTTS
from datetime import datetime

def text_to_speech(text:str):
    now = datetime.now()
    tts = SileroTTS(model_id='v5_ru', language='ru', sample_rate=48000, device='cpu')
    tts.tts(text, f'output/output_{now.hour}_{now.minute}.wav')