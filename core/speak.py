from loguru import logger
# Импортируем класс SileroTTS для синтеза речи из текста
from silero_tts.silero_tts import SileroTTS 
# Импортируем утилиту для формирования пути к выходному файлу
from utils.utils import form_output_data

# Создаем отдельный логгер для данного модуля, указывая имя (например, для фильтрации логов)
speak_module_logger = logger.bind(name="listen_module")
speak_module_logger.info("INIT")  # Логируем факт инициализации модуля

def speak(answer: str) -> str:
    """
    Преобразует переданный текст в аудиофайл (wav) с помощью модели SileroTTS.
    
    :param answer: Текстовый ответ, который необходимо преобразовать в речь.
    :return: Путь к сгенерированному аудиофайлу (формат wav).
    """
    
    # Инициализация синтезатора речи
    tts = SileroTTS(
        model_id='v5_ru',      # Версия и язык модели (русский)
        language='ru',
        sample_rate=24000,     # Частота дискретизации аудио
        device='cpu',          # Устройство для вычислений (CPU)
        speaker="eugene"       # Используемый голос для синтеза
    )

    speak_module_logger.info("init tts")

    # Формируем уникальный путь к выходному аудиофайлу с расширением 'wav'
    output_filepath = form_output_data()

    speak_module_logger.info("start gen speach")
    # Синтезируем речь и сохраняем её в указанный файл
    tts.tts(answer, output_filepath)

    speak_module_logger.info("finish gen speach")

    # Возвращаем путь к готовому аудиофайлу
    return output_filepath