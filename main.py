import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from handlers.text_handler import handle_text
from handlers.image_handler import handle_image
from handlers.voice_handler import handle_voice
from handlers.start_handler import handle_start
from handlers.callback_handler import handle_callback
from utils.keep_alive import keep_alive

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN not found in .env file. Exiting.")
        exit(1)

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register Handlers
    start_handler = CommandHandler('start', handle_start)
    callback_handler = CallbackQueryHandler(handle_callback)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text)
    image_handler = MessageHandler(filters.PHOTO, handle_image)
    voice_handler = MessageHandler(filters.VOICE, handle_voice)

    application.add_handler(start_handler)
    application.add_handler(callback_handler)
    application.add_handler(text_handler)
    application.add_handler(image_handler)
    application.add_handler(voice_handler)

    print("🤖 Bot is running...")
    keep_alive()  # Start the web server
    print("📢 Required channel: @RISK_VIR")
    application.run_polling()
