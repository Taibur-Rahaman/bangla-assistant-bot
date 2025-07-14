import os
import whisper
import ffmpeg
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Get bot token from Render environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

model = whisper.load_model("base")

def convert_ogg_to_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)

def transcribe(file_path):
    result = model.transcribe(file_path, language="bn")
    return result["text"]

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"
    await voice.download_to_drive(ogg_path)
    convert_ogg_to_wav(ogg_path, wav_path)
    text = transcribe(wav_path)
    await update.message.reply_text(f"আপনার বার্তা:\n{text}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

app.run_polling()

