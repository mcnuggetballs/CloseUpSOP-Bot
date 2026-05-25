import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from database import (
    get_connection
)

from config import (
    GROUP_CHAT_ID,
    TOPIC_ID,
    TIMEZONE
)


# ==========================
# TIME
# ==========================

def now():

    return (
        datetime
        .now(
            ZoneInfo(
                TIMEZONE
            )
        )
    )


# ==========================
# SAVE SESSION
# ==========================

def save_log(
    user_id,
    user,
    date,
    timestamp
):

    conn = get_connection()

    c = conn.cursor()

    c.execute(
        """
        INSERT INTO closeup_logs
        (
            telegram_user_id,
            user_name,
            date,
            completion_timestamp
        )
        VALUES
        (?,?,?,?)
        """,
        (
            user_id,
            user,
            date,
            timestamp
        )
    )

    log_id = c.lastrowid

    conn.commit()

    conn.close()

    return log_id


# ==========================
# SAVE PHOTOS
# ==========================

def save_photos(
    log_id,
    photos
):

    conn = get_connection()

    c = conn.cursor()

    for index, photo in enumerate(
        photos
    ):

        c.execute(
            """
            INSERT INTO closeup_photos
            (
                closeup_log_id,
                step_number,
                telegram_file_id
            )
            VALUES
            (?,?,?)
            """,
            (
                log_id,
                index + 1,
                photo
            )
        )

    conn.commit()

    conn.close()


# ==========================
# SEND GROUP REPORT
# ==========================

async def send_report(
    context,
    user,
    timestamp,
    photos
):

    caption = (
        f"{user} "
        f"has closed up "
        f"the venue.\n\n"
        f"{timestamp}"
    )

    await (
        context
        .bot
        .send_message(
            chat_id=GROUP_CHAT_ID,
            text=caption,
            message_thread_id=TOPIC_ID
        )
    )

    for photo in photos:

        try:

            await (
                context
                .bot
                .send_photo(
                    chat_id=GROUP_CHAT_ID,
                    photo=photo,
                    message_thread_id=TOPIC_ID,
                    write_timeout=120,
                    connect_timeout=30
                )
            )

            await asyncio.sleep(
                0.4
            )

        except Exception as e:

            print(
                f"Photo upload failed: {e}"
            )

# ==========================
# COMPLETE
# ==========================

async def complete(
    update,
    context
):

    user = (
        update
        .effective_user
        .first_name
    )

    current = now()

    date = (
        current
        .strftime(
            "%d/%m/%Y"
        )
    )

    timestamp = (
        current
        .strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    photos = (
        context
        .user_data[
            "closeup_images"
        ]
    )

    log_id = (
        save_log(
            update
            .effective_user
            .id,
            user,
            date,
            timestamp
        )
    )

    save_photos(
        log_id,
        photos
    )

    await send_report(
        context,
        user,
        timestamp,
        photos
    )

    context.user_data.pop(
        "closeup_images",
        None
    )

    context.user_data.pop(
        "closeup_step",
        None
    )

    context.user_data[
        "screen"
    ] = "menu"

    return True