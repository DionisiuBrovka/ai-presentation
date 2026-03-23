import os
from loguru import logger
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")
_client = Groq(api_key=API_KEY)

def think(question:str) -> str:
    with open("promts/system_promt.txt", "r") as file:
        system_promt = file.read()

    completion = _client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
        {
            "role": "system",
            "content": system_promt
        },
        {
            "role": "user",
            "content": question
        }
        ],
        temperature=1,
        max_completion_tokens=2500,
        top_p=1,
        reasoning_effort="low",
        stream=False,
        stop=None,
        tools=[{"type":"browser_search"}]
    )

    return str(completion.choices[0].message.content)