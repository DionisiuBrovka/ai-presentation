#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime
from pathlib import Path

from silero_tts.silero_tts import SileroTTS


def get_text(args):
    # 1. Если передали текст аргументом
    if args.text:
        return args.text

    # 2. Если передали файл
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()

    # 3. Если пайп (stdin)
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # 4. Ошибка
    print("❌ Нет текста. Передай --text, --file или используй pipe.")
    sys.exit(1)


def generate_output_path(output_dir):
    now = datetime.now()
    filename = f"output-{now.strftime('%H_%M_%d_%m_%Y')}.wav"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return str(Path(output_dir) / filename)


def main():
    parser = argparse.ArgumentParser(description="Быстрый TTS через Silero")
    parser.add_argument("-t", "--text", help="Текст для озвучки")
    parser.add_argument("-f", "--file", help="Файл с текстом")
    parser.add_argument("-o", "--output", help="Имя выходного файла")
    parser.add_argument("-s", "--speaker", default="eugene", help="Голос")
    parser.add_argument("--rate", type=int, default=24000, help="Sample rate")

    args = parser.parse_args()

    text = get_text(args)

    output_path = args.output or generate_output_path("output")

    print(f"▶ Генерация: {output_path}")

    tts = SileroTTS(
        model_id="v5_ru",
        language="ru",
        sample_rate=args.rate,
        device="cpu",
        speaker=args.speaker
    )

    tts.tts(text, output_path)

    print("✅ Готово!")


if __name__ == "__main__":
    main()