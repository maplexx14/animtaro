import asyncio
import json
import logging
import os
import random
from pathlib import Path
from uuid import uuid4

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultCachedPhoto, Message


logging.basicConfig(level=logging.INFO)

FILE_IDS_PATH = Path("photo_file_ids.json")


def get_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")
    return token


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


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Этот бот работает в inline-режиме.\n"
        "Напиши в любом чате: @your_bot_username"
    )


@dp.inline_query(F.query.regexp(r"^.*$"))
async def inline_random_image(query: InlineQuery) -> None:
    photo_file_id = random.choice(load_photo_file_ids())

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


async def main() -> None:
    bot = Bot(token=get_token())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
