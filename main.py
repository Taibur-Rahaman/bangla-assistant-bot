import os
import openai
import ffmpeg
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.environ.get("PORT", "8080"))  # Railway uses PORT env var
APP_URL = os.getenv("RAILWAY_PUBLIC_URL")   # Add this in Railway Variables

openai.api_key = OPENAI_API_KEY

def convert_ogg_to_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"
    await voice.download_to_drive(ogg_path)
    convert_ogg_to_wav(ogg_path, wav_path)

    with open(wav_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="bn")

    text = transcript["text"]
    await update.message.reply_text(f"আপনার বার্তা:\n{text}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Set webhook
    await app.bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{APP_URL}/{BOT_TOKEN}",
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
