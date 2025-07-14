import os
import openai
import ffmpeg
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def convert_ogg_to_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Voice message received.")
    voice = await update.message.voice.get_file()
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"
    await voice.download_to_drive(ogg_path)

    convert_ogg_to_wav(ogg_path, wav_path)

    with open(wav_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="bn")
    
    text = transcript["text"]
    logging.info(f"Transcribed text: {text}")
    await update.message.reply_text(f"আপনার বার্তা:\n{text}")

if BOT_TOKEN is None:
    print("❌ BOT_TOKEN is not set.")
else:
    print("✅ Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling()
