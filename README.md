# Telegram inline bot on aiogram

Бот отвечает на inline-запрос одной случайной картинкой из набора `file_id`, уже загруженных в Telegram.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка

1. Создай бота через `@BotFather`.
2. Включи inline mode командой `/setinline`.
3. Задай токен:

```bash
export BOT_TOKEN="твой_токен"
```

4. `file_id` должны быть получены именно этим ботом. Если взять `file_id` от другого бота или аккаунта, Telegram может вернуть `PHOTO_INVALID`.
5. Положи картинки в папку `images/`, задай `CHAT_ID` и запусти:

```bash
mkdir -p images
export CHAT_ID="твой_chat_id"
python3 upload_photos.py
```

6. Скрипт сам сохранит `file_id` в [photo_file_ids.json](/Users/maplex/test/photo_file_ids.json). Бот читает этот файл автоматически, вручную ничего копировать не нужно.

## Запуск

```bash
python3 main.py
```

## Как использовать

В любом чате Telegram введи:

```text
@username_твоего_бота
```

На каждый inline-запрос бот вернет одну случайную картинку.
