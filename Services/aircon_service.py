from datetime import datetime
from zoneinfo import ZoneInfo

from database import (
    get_connection
)

from config import (
    GROUP_CHAT_ID,
    TIMEZONE,
    TOPIC_ID
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
        .strftime(
            "%d/%m/%Y %H:%M"
        )
    )


# ==========================
# SAVE STATUS
# ==========================

def update_status(
    aircon,
    status,
    user,
    timestamp,
    photo=None
):

    conn = get_connection()

    c = conn.cursor()

    c.execute(
        """
        INSERT OR REPLACE
        INTO aircon_status
        VALUES
        (?,?,?,?,?)
        """,
        (
            aircon,
            status,
            user,
            timestamp,
            photo
        )
    )

    conn.commit()

    conn.close()


# ==========================
# SAVE LOG
# ==========================

def save_log(
    user_id,
    user,
    aircon,
    action,
    timestamp,
    photo=None
):

    conn = get_connection()

    c = conn.cursor()

    c.execute(
        """
        INSERT INTO aircon_logs
        (
            telegram_user_id,
            user_name,
            aircon_name,
            action,
            timestamp,
            photo_file_id
        )
        VALUES
        (?,?,?,?,?,?)
        """,
        (
            user_id,
            user,
            aircon,
            action,
            timestamp,
            photo
        )
    )

    conn.commit()

    conn.close()


# ==========================
# GROUP REPORT
# ==========================

async def report(
    context,
    message,
    photo=None
):

    if photo:

        await (
            context
            .bot
            .send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=photo,
                caption=message,
                message_thread_id=TOPIC_ID
            )
        )

        return

    await (
        context
        .bot
        .send_message(
            chat_id=GROUP_CHAT_ID,
            text=message,
            message_thread_id=TOPIC_ID
        )
    )

def get_current_status(
    aircon
):

    conn = get_connection()

    c = conn.cursor()

    c.execute(
        """
        SELECT status
        FROM aircon_status
        WHERE aircon_name=?
        """,
        (
            aircon,
        )
    )

    row = c.fetchone()

    conn.close()

    if row:
        return row["status"]

    return None

# ==========================
# ON
# ==========================

async def turn_on(
    update,
    context
):

    aircon = (
        context
        .user_data[
            "selected_aircon"
        ]
    )

    user = (
        update
        .effective_user
        .first_name
    )

    timestamp = now()

    current = get_current_status(
        aircon
    )

    if current == "ON":
        return False

    update_status(
        aircon,
        "ON",
        user,
        timestamp
    )

    save_log(
        update
        .effective_user
        .id,
        user,
        aircon,
        "ON",
        timestamp
    )

    await report(
        context,
        (
            f"{aircon} "
            f"has been turned ON\n\n"
            f"By: {user}\n"
            f"Time: {timestamp}"
        )
    )
    
    return True


# ==========================
# OFF
# ==========================

async def turn_off(
    update,
    context,
    photo
):

    aircon = (
        context
        .user_data[
            "selected_aircon"
        ]
    )

    user = (
        update
        .effective_user
        .first_name
    )

    timestamp = now()
    current = get_current_status(
        aircon
    )

    if current == "OFF":

        return False

    update_status(
        aircon,
        "OFF",
        user,
        timestamp,
        photo
    )

    save_log(
        update
        .effective_user
        .id,
        user,
        aircon,
        "OFF",
        timestamp,
        photo
    )

    msg = (
        f"{aircon} "
        f"has been turned OFF\n\n"
        f"By: {user}\n"
        f"Time: {timestamp}"
    )

    await report(
        context,
        msg,
        photo
    )
    
    return True