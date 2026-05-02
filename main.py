import os
import asyncio
import requests
from telethon import TelegramClient, events

# Variables de entorno
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Crear cliente
client = TelegramClient("session", API_ID, API_HASH)

async def main():
    print("Userbot iniciado...")

    @client.on(events.NewMessage)
    async def handler(event):
        try:
            message_text = event.raw_text

            if not message_text:
                return

            payload = {
                "source": "telegram_userbot",
                "chat_id": event.chat_id,
                "text": message_text
            }

            requests.post(WEBHOOK_URL, json=payload, timeout=10)

        except Exception as e:
            print("Error:", e)

    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
