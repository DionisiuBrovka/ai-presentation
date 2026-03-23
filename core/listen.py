import os
from loguru import logger
from groq import Groq

listen_module_logger = logger.bind(name="listen_module")
listen_module_logger.info("INIT")

API_KEY = os.getenv("GROQ_API_KEY")
_client = Groq(api_key=API_KEY)


def listen(filename:str) -> str:
    listen_module_logger.info("start listen")
    with open(filename, "rb") as file:
        listen_module_logger.info(f"open file -> {filename}")
        transcription = _client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        temperature=0,
        language="ru",
        response_format="verbose_json",
        )
    listen_module_logger.info("close file")
    return transcription.text