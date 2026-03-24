import random
from datetime import datetime

from werkzeug.datastructures import FileStorage

def get_random_test_audio() -> str:
    """
    Возвращает путь к случайному тестовому аудиофайлу из заранее определённого списка.
    
    :return: Путь к одному из тестовых аудиофайлов.
    """
    random_test_audio_list = [
        'test-audio/test-audio-1.ogg',
        'test-audio/test-audio-2.ogg',
        'test-audio/test-audio-3.ogg',
    ]

    return random.choice(random_test_audio_list)

def form_input_data(file: FileStorage):
    """
    Формирует путь и имя для загружаемого входного файла на основе текущей даты и времени.
    
    :param file: Объект FileStorage, представляющий загруженный пользователем файл.
    :return: Кортеж (полный путь к файлу, имя файла, формат файла).
    """
    now = datetime.now()
    # Извлекаем расширение файла (формат), если оно имеется
    input_fileformat = file.filename.split('.')[-1] if '.' in file.filename else ''
    # Генерируем уникальное имя файла с использованием текущего времени и даты
    input_filename = f"input-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}_{now.microsecond}.{input_fileformat}"
    # Полный путь для сохранения файла
    input_filepath = f"input/{input_filename}"

    return input_filepath, input_filename, input_fileformat

def form_output_data() -> str:
    """
    Формирует путь и имя для выходного (обработанного) аудиофайла, используя текущие дату и время.
    
    :return: Полный путь к выходному аудиофайлу формата .wav.
    """
    now = datetime.now()
    # Имя файла с уникальным идентификатором времени
    return f"output/output-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}.wav"