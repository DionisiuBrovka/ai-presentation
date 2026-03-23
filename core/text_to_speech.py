from silero_tts.silero_tts import SileroTTS
from datetime import datetime

def text_to_speech(text:str) -> str:
    now = datetime.now()
    tts = SileroTTS(model_id='v5_ru', language='ru', sample_rate=48000, device='cpu')
    output_filename = f'output/output_{now.hour}_{now.minute}.wav'
    tts.tts(text, output_filename)
    return output_filename