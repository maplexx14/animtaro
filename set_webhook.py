import asyncio
import os

from aiogram import Bot

from main import WEBHOOK_PATH, get_required_env


async def main() -> None:
    bot = Bot(token=get_required_env("BOT_TOKEN"))
    public_base_url = get_required_env("PUBLIC_BASE_URL").rstrip("/")
    webhook_secret = get_required_env("WEBHOOK_SECRET")
    webhook_url = f"{public_base_url}{WEBHOOK_PATH}"

    try:
        await bot.set_webhook(
            url=webhook_url,
            secret_token=webhook_secret,
            drop_pending_updates=True,
        )
        print(f"Webhook set to {webhook_url}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
