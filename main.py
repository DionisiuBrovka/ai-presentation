# Импорт функции загрузки переменных окружения из .env-файла
from flask.cli import load_dotenv  

# Загрузка переменных окружения (например, ключей API, настроек доступа и т.д.)
load_dotenv()

# Импорт базовых компонентов Flask: веб-сервер, обработка файлов и запросов
from flask import Flask, send_file, request

# Импорт бизнес-логики (собственные модули в пакете core)
from core.listen import listen   # Модуль для чтения аудио и получения "сырого" аудиоввода
from core.think import think     # Модуль для обработки ввода (например, распознавание речи, генерация ответа)
from core.speak import speak     # Модуль для преобразования текста в аудио (wav)

# Импорт утилиты для формирования безопасного пути и имени сохраняемого файла
from utils.utils import form_input_data, form_output_data

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

@app.route("/ask/", methods=['POST'])
def ask():
    """
    Эндпоинт для обработки пользовательского запроса с аудиофайлом.
    Принимает POST-запрос с файлом, проводит обработку через пайплайн listen→think→speak.
    На выходе отдает готовый аудиофайл (wave).
    """

    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    # Получаем объект FileStorage из запроса
    file = request.files['file']

    # Проверяем, был ли выбран файл пользователем
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # Формируем путь, имя и формат файла для сохранения
    input_filepath, input_filename, input_fileformat = form_input_data(file)

    # Сохраняем загруженный файл во временную директорию на диск
    file.save(input_filepath)

    # Основная цепочка обработки данных:
    # 1. listen - извлекаем данные из файла
    # 2. think  - обрабатываем полученные данные (например, распознаём речь и генерируем ответ)
    # 3. speak  - преобразуем текстовый результат обратно в аудио (wav)
    processed_wav_path = speak(think(listen(input_filepath)))

    # Возвращаем пользователю готовый обработанный wav-файл
    return send_file(
        processed_wav_path,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="processed_audio.wav"
    )

if __name__ == '__main__':
    # Запуск приложения в режиме отладки.
    # Flask автоматически перезапускается при изменениях кода — удобно для тестирования и разработки.
    app.run(debug=True)