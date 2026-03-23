import random
from datetime import datetime

def get_random_test_audio() -> str:
    random_test_audio_list = [
        'test-audio/test-audio-1.ogg',
        'test-audio/test-audio-2.ogg',
        'test-audio/test-audio-3.ogg',
    ]

    return random.choice(random_test_audio_list)


# TODO доделать удаление имени и сохранение формата
def form_input_filename(filename:str) -> str:
    now = datetime.now()
    return f"input/input-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}-{filename}"

def form_output_filename(format:str) -> str:
    now = datetime.now()
    return f"output/output-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}.{format}"