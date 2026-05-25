import os

from dotenv import (
    load_dotenv
)

load_dotenv()

BOT_TOKEN = (
    os.getenv(
        "BOT_TOKEN"
    )
)

GROUP_CHAT_ID = int(
    os.getenv(
        "GROUP_CHAT_ID"
    )
)

TOPIC_ID = int(
    os.getenv(
        "TOPIC_ID"
    )
)

TIMEZONE = (
    os.getenv(
        "TIMEZONE"
    )
)

DATABASE_NAME = (
    os.getenv(
        "DATABASE_NAME",
        "closeup.db"
    )
)