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

4. Задай публичный адрес приложения и секрет вебхука:

```bash
export PUBLIC_BASE_URL="https://yourusername.pythonanywhere.com"
export WEBHOOK_SECRET="случайная_длинная_строка"
```

5. `file_id` должны быть получены именно этим ботом. Если взять `file_id` от другого бота или аккаунта, Telegram может вернуть `PHOTO_INVALID`.
6. Положи картинки в папку `images/`, задай `CHAT_ID` и запусти:

```bash
mkdir -p images
export CHAT_ID="твой_chat_id"
python3 upload_photos.py
```

7. Скрипт сам сохранит `file_id` в [photo_file_ids.json](/Users/maplex/test/photo_file_ids.json). Бот читает этот файл автоматически, вручную ничего копировать не нужно.

## Запуск

### Локально

```bash
flask --app main run --debug
python3 set_webhook.py
```

### PythonAnywhere

1. Загрузи проект в домашнюю директорию PythonAnywhere.
2. Создай virtualenv и установи зависимости:

```bash
mkvirtualenv --python=/usr/bin/python3.11 telegram-inline-bot
pip install -r requirements.txt
```

3. На вкладке `Web` создай Flask web app.
4. В качестве WSGI entrypoint используй [passenger_wsgi.py](/Users/maplex/test/passenger_wsgi.py).
5. В разделе `Environment variables` добавь:

```text
BOT_TOKEN=...
PUBLIC_BASE_URL=https://yourusername.pythonanywhere.com
WEBHOOK_SECRET=...
```

6. В Bash console активируй virtualenv и выполни:

```bash
python3 set_webhook.py
```

7. Нажми `Reload`.

## Ограничение PythonAnywhere free

На бесплатном плане PythonAnywhere у кода только доступ к allowlisted сайтам, а у paid plans - unrestricted Internet access ([PythonAnywhere pricing](https://www.pythonanywhere.com/pricing/), [allowlist](https://www.pythonanywhere.com/whitelist/)). Для Telegram-бота это критично, потому что приложению нужен исходящий доступ к Bot API. Значит, для этого webhook-бота нужен paid PythonAnywhere, а не free.

## Как использовать

В любом чате Telegram введи:

```text
@username_твоего_бота
```

На каждый inline-запрос бот вернет одну случайную картинку.
