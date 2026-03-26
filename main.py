import os
from datetime import datetime

# Импортируем класс основной веб-фреймворк
from flask import Flask, send_file, request
from flask.cli import load_dotenv  

# Библиотека для работы с groq
from groq import Groq
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")# Получаем API-ключ для сервиса Groq из переменных окружения
_client = Groq(api_key=API_KEY)# Инициализируем клиента Groq для дальнейшей работы с API

# Импортируем класс SileroTTS для синтеза речи из текста
from silero_tts.silero_tts import SileroTTS 

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

@app.route("/ask/", methods=['POST'])
def ask():
    """
    Эндпоинт для обработки пользовательского запроса с аудиофайлом.
    Принимает POST-запрос с файлом, проводит обработку через пайплайн listen→think→speak.
    На выходе отдает готовый аудиофайл (wave).
    """

    # ---------------------------------------------------------------------

    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    # Получаем объект FileStorage из запроса
    file = request.files['file']

    # Проверяем, был ли выбран файл пользователем
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # Формируем путь, имя и формат файла для сохранения
    now = datetime.now()
    input_fileformat = file.filename.split('.')[-1] if '.' in file.filename else ''
    input_filename = f"input-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}_{now.microsecond}.{input_fileformat}"
    input_filepath = f"input/{input_filename}"

    # Сохраняем загруженный файл во временную директорию на диск
    file.save(input_filepath)

    # ---------------------------------------------------------------------

    # 1. listen - извлекаем данные из файла
    with open(input_filepath, "rb") as file:

        # Отправляем файл на распознавание речи (транскрипцию) через API Groq
        transcription = _client.audio.transcriptions.create(
            file=(input_filepath, file.read()),      # Передаем имя и содержимое файла
            model="whisper-large-v3",          # Указываем используемую модель
            temperature=0,                     # Температура генерации (экспериментальный параметр, обычно 0)
            language="ru",                     # Язык исходного аудио (русский)
            response_format="verbose_json",    # Формат ответа — подробный JSON
        )

    # ---------------------------------------------------------------------

    # 2. think  - обрабатываем полученные данные (например, распознаём речь и генерируем ответ)
    with open("promts/system_promt.txt", "r") as file:
        system_promt = file.read()

    completion = _client.chat.completions.create(
        model="openai/gpt-oss-120b",   # Указываем модель
        messages=[
            {
                "role": "system",
                "content": system_promt   # Системное сообщение — влияет на общий стиль и возможности ассистента
            },
            {
                "role": "user",
                "content": transcription.text       # Сообщение пользователя — конкретный запрос для генерации ответа
            }
        ],
        temperature=1,                   # Температура генерации (вариативность; 1 — относительно высокая креативность)
        max_completion_tokens=2500,      # Максимальная длина сгенерированного ответа, в токенах
        top_p=1,
        reasoning_effort="low",          # (Параметр модели: степень проработки рассуждений. "low" — быстро и просто.)
        stream=False,                    # Стриминг отключён: ответ приходит целиком
        stop=None,                       # Нет дополнительных стоп-слов
        tools=[{"type": "browser_search"}] # Доступны инструменты поиска (если реализовано в модели)
    )

    # ---------------------------------------------------------------------

    # 3. speak  - преобразуем текстовый результат обратно в аудио (wav)
    tts = SileroTTS(
        model_id='v5_ru',      # Версия и язык модели (русский)
        language='ru',
        sample_rate=24000,     # Частота дискретизации аудио
        device='cpu',          # Устройство для вычислений (CPU)
        speaker="eugene"       # Используемый голос для синтеза
    )

    # Формируем уникальный путь к выходному аудиофайлу с расширением 'wav'
    output_filepath = f"output/output-{now.hour}_{now.minute}_{now.day}_{now.month}_{now.year}.wav"

    # Синтезируем речь и сохраняем её в указанный файл
    tts.tts(str(completion.choices[0].message.content), output_filepath)

    # ---------------------------------------------------------------------

    # Возвращаем пользователю готовый обработанный wav-файл
    return send_file(
        output_filepath,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="processed_audio.wav"
    )

if __name__ == '__main__':
    # Запуск приложения в режиме отладки.
    # Flask автоматически перезапускается при изменениях кода — удобно для тестирования и разработки.
    app.run(debug=True)