import os
from loguru import logger
from groq import Groq

# Создаем отдельный логгер для данного модуля, указывая имя (например, для фильтрации логов)
listen_module_logger = logger.bind(name="listen_module")
listen_module_logger.info("INIT")  # Логируем факт инициализации модуля

# Получаем API-ключ для сервиса Groq из переменных окружения
API_KEY = os.getenv("GROQ_API_KEY")
_client = Groq(api_key=API_KEY)  # Инициализируем клиента Groq для дальнейшей работы с API

def listen(filepath: str) -> str:
    """
    Принимает на вход имя (путь к) аудиофайла, выполняет его транскрибацию с помощью модели Whisper через сервис Groq.
    
    :param filename: Путь к аудиофайлу для распознавания речи.
    :return: Распознанный текст.
    """
    listen_module_logger.info("start listen")
    
    # Открываем файл в режиме бинарного чтения
    with open(filepath, "rb") as file:
        listen_module_logger.info(f"open file -> {filepath}")
        # Отправляем файл на распознавание речи (транскрипцию) через API Groq
        transcription = _client.audio.transcriptions.create(
            file=(filepath, file.read()),      # Передаем имя и содержимое файла
            model="whisper-large-v3",          # Указываем используемую модель
            temperature=0,                     # Температура генерации (экспериментальный параметр, обычно 0)
            language="ru",                     # Язык исходного аудио (русский)
            response_format="verbose_json",    # Формат ответа — подробный JSON
        )
    listen_module_logger.info("close file")
    return transcription.text  # Возвращаем распознанный текст (ключ "text")