from silero_tts.silero_tts import SileroTTS
from utils.utils import form_output_filename

def speak(anser:str) -> str:

    tts = SileroTTS(
        model_id='v5_ru', 
        language='ru', 
        sample_rate=24000, 
        device='cpu', 
        speaker="eugene"
    )

    output_filename = form_output_filename("wav")
    tts.tts(anser, output_filename)

    return output_filename