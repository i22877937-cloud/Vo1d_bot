#!/usr/bin/env python3
import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "ТВОЙ_ТОКЕН"

DUCKY_SCRIPT = """GUI r
DELAY 300
STRING voice control
ENTER
DELAY 2000
STRING shut down
ENTER
DELAY 1500
STRING turn off
ENTER
DELAY 1500"""

async def start(update: Update, context):
    await update.message.reply_text("Отправь /code — получу inject.bin")

async def send_code(update: Update, context):
    filename = "inject.bin"
    with open(filename, "w") as f:
        f.write(DUCKY_SCRIPT)
    with open(filename, "rb") as f:
        await update.message.reply_document(document=InputFile(f, filename=filename))
    os.remove(filename)

def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", send_code))
    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
