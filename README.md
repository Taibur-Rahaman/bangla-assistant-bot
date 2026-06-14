# Bangla Assistant Bot

A Telegram bot that transcribes Bengali voice messages to text using OpenAI Whisper.

## Overview

Send a voice note in Bangla on Telegram and the bot converts it to written text — useful for accessibility, note-taking, and quick transcription without typing.

## Features

- Voice message handling via Telegram Bot API
- OGG → WAV conversion with FFmpeg
- Bengali speech-to-text via OpenAI Whisper (`whisper-1`)
- Webhook deployment (designed for Railway and similar PaaS hosts)

## Tech Stack

- **Python 3**
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (webhooks)
- [OpenAI API](https://platform.openai.com/) (Whisper)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

## Prerequisites

- Python 3.9+
- FFmpeg installed on the system (`ffmpeg` available in PATH)
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- OpenAI API key

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram bot token from BotFather |
| `OPENAI_API_KEY` | OpenAI API key for Whisper |
| `PORT` | HTTP port for the webhook server (default: `8080`) |
| `RAILWAY_PUBLIC_URL` | Public HTTPS URL of the deployed app (used for webhook registration) |

## Local Development

```bash
git clone https://github.com/Taibur-Rahaman/bangla-assistant-bot.git
cd bangla-assistant-bot

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

export BOT_TOKEN="your-telegram-bot-token"
export OPENAI_API_KEY="your-openai-api-key"
export RAILWAY_PUBLIC_URL="https://your-public-url.example.com"

python main.py
```

The bot runs in webhook mode. For local testing you typically need a tunnel (e.g. ngrok) so Telegram can reach your machine.

## Deploy on Railway

1. Push this repo to GitHub.
2. Create a new Railway project and connect the repository.
3. Set `BOT_TOKEN`, `OPENAI_API_KEY`, and `RAILWAY_PUBLIC_URL` (Railway provides the public URL automatically).
4. Deploy — the `Procfile` starts the webhook server.

## Usage

1. Open your bot on Telegram.
2. Send a **voice message** in Bangla.
3. The bot replies with the transcribed text prefixed by `আপনার বার্তা:`.

## Project Structure

```
bangla-assistant-bot/
├── main.py              # Bot entry point (webhook + voice handler)
├── requirements.txt     # Python dependencies
├── Procfile             # Railway process definition
└── README.md
```

## Author

**Md Taibur Rahaman** — [GitHub](https://github.com/Taibur-Rahaman)

## License

MIT
