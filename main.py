import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"
    await voice.download_to_drive(ogg_path)
    # Convert ogg to wav - use ffmpeg as before
    import ffmpeg
    ffmpeg.input(ogg_path).output(wav_path).run(overwrite_output=True)
    
    # Read audio bytes
    with open(wav_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="bn")
    
    text = transcript["text"]
    await update.message.reply_text(f"আপনার বার্তা:\n{text}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

app.run_polling()
