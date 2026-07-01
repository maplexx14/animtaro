import json
import os
import random
from pathlib import Path
from uuid import uuid4

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultCachedPhoto, Message, Update
from flask import Flask, Response, request


BASE_DIR = Path(__file__).resolve().parent
FILE_IDS_PATH = BASE_DIR / "photo_file_ids.json"


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def load_photo_file_ids() -> list[str]:
    if not FILE_IDS_PATH.exists():
        raise RuntimeError(
            f"{FILE_IDS_PATH} not found. Run upload_photos.py first to generate file_id values."
        )

    with FILE_IDS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list) or not data or not all(isinstance(item, str) for item in data):
        raise RuntimeError(f"{FILE_IDS_PATH} must contain a non-empty JSON array of strings")

    return data


BOT_TOKEN = get_required_env("BOT_TOKEN")
WEBHOOK_SECRET = get_required_env("WEBHOOK_SECRET")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
PHOTO_FILE_IDS = load_photo_file_ids()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = Flask(__name__)


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Этот бот работает в inline-режиме.\n"
        "Напиши в любом чате: @your_bot_username"
    )


@dp.inline_query(F.query.regexp(r"^.*$"))
async def inline_random_image(query: InlineQuery) -> None:
    photo_file_id = random.choice(PHOTO_FILE_IDS)

    result = InlineQueryResultCachedPhoto(
        id=str(uuid4()),
        photo_file_id=photo_file_id,
        title="Случайная картинка",
        description="Одна из случайных картинок",
    )

    await query.answer(
        results=[result],
        cache_time=1,
        is_personal=True,
    )


@app.post(WEBHOOK_PATH)
def telegram_webhook() -> Response:
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != WEBHOOK_SECRET:
        return Response(status=403)

    update = Update.model_validate(request.get_json())
    import asyncio

    asyncio.run(dp.feed_update(bot, update))
    return Response(status=200)


@app.get("/")
def healthcheck() -> tuple[str, int]:
    return "ok", 200


if __name__ == "__main__":
    app.run()
