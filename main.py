import os
import asyncio
import requests
from telethon import TelegramClient, events
from flask import Flask

# Variables de entorno
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Crear cliente Telegram
client = TelegramClient("session", API_ID, API_HASH)

# Crear app Flask mínima
app = Flask(__name__)

@app.route("/")
def home():
    return "Userbot activo"

async def telegram_listener():
    await client.connect()

    if not await client.is_user_authorized():
        print("⚠️ Sesión no autorizada")
        return

    print("✅ Userbot conectado correctamente")

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

def run():
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_listener())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    run()
