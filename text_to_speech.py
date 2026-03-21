from silero_tts.silero_tts import SileroTTS

def text_to_speech(text:str):
    tts = SileroTTS(model_id='v5_ru', language='ru', sample_rate=48000, device='cpu')
    tts.tts(text, 'output.wav')