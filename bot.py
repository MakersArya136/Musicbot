import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import youtube_dl

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token from BotFather
TOKEN = '7418354648:AAHS7ouwQVgCo9jildCo5tb6gvul_oWo4kE'

async def start(update: Update, context) -> None:
    await update.message.reply_text('Hello! I can play music and videos. Send me a link!')

async def download_audio(update: Update, context) -> None:
    url = ' '.join(context.args)  # Get the URL from the message
    if not url:
        await update.message.reply_text('Please provide a URL')
        return
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            await update.message.reply_text(f'Download complete: {filename}')

    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')

async def download_video(update: Update, context) -> None:
    url = ' '.join(context.args)
    if not url:
        await update.message.reply_text('Please provide a URL')
        return
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            await update.message.reply_text(f'Video Downloaded: {filename}')
            await update.message.reply_video(open(filename, 'rb'))
    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", download_audio))
    application.add_handler(CommandHandler("video", download_video))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
