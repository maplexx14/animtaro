import asyncio
import json
import os
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile


IMAGE_DIR = Path("images")
FILE_IDS_PATH = Path("photo_file_ids.json")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


async def main() -> None:
    bot = Bot(token=get_required_env("BOT_TOKEN"))
    chat_id = int(get_required_env("CHAT_ID"))

    image_paths = sorted(
        path
        for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_paths:
        raise RuntimeError(f"No images found in {IMAGE_DIR}")

    file_ids = []

    try:
        for path in image_paths:
            message = await bot.send_photo(chat_id=chat_id, photo=FSInputFile(path))
            file_id = message.photo[-1].file_id
            file_ids.append(file_id)
            print(f"{path.name}: {file_id}")
    finally:
        await bot.session.close()

    with FILE_IDS_PATH.open("w", encoding="utf-8") as file:
        json.dump(file_ids, file, ensure_ascii=True, indent=2)

    print(f"Saved {len(file_ids)} file_id values to {FILE_IDS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
