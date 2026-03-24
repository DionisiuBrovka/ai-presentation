import os
from loguru import logger
from groq import Groq

# Создаем отдельный логгер для данного модуля, указывая имя (например, для фильтрации логов)
think_module_logger = logger.bind(name="think_module")
think_module_logger.info("INIT")  # Логируем факт инициализации модуля

# Получаем API-ключ для сервиса Groq из переменных окружения
API_KEY = os.getenv("GROQ_API_KEY")
# Инициализируем клиента Groq для общения с моделью
_client = Groq(api_key=API_KEY)

def think(question: str) -> str:
    """
    Функция получения текстового ответа от модели ИИ на основе пользовательского вопроса
    и системного prompt-а (описания поведения бота).
    
    :param question: Пользовательский вопрос (строка).
    :return: Ответ, сгенерированный моделью, в виде строки.
    """

    # Считываем системный промт (описание ролей, задач, поведения ИИ) из внешнего файла
    with open("promts/system_promt.txt", "r") as file:
        system_promt = file.read()

    think_module_logger.info("get system promt")

    think_module_logger.info("start think")
    # Формируем запрос к языковой модели
    completion = _client.chat.completions.create(
        model="openai/gpt-oss-120b",   # Указываем модель
        messages=[
            {
                "role": "system",
                "content": system_promt   # Системное сообщение — влияет на общий стиль и возможности ассистента
            },
            {
                "role": "user",
                "content": question       # Сообщение пользователя — конкретный запрос для генерации ответа
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

    think_module_logger.info(f"finish thinking -> anser is {len(completion.choices[0].message.content)} char length")
    # Возвращаем содержимое первого (и скорее всего единственного) сообщения-ответа модели
    return str(completion.choices[0].message.content)