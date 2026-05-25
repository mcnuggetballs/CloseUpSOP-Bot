from telegram.ext import (
ApplicationBuilder,
CallbackQueryHandler,
MessageHandler,
CommandHandler,
filters
)

from config import BOT_TOKEN
from database import init_db
from Screens.start import start
from Services.scheduler import start_scheduler

from state_engine import (
handle_text,
handle_callback,
handle_photo
)

def main():

    init_db()

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )
    print("Bot started")
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handle_callback
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT,
            handle_text
        )
    )
    start_scheduler(app)
    app.run_polling()


if __name__ == "__main__":
    main()