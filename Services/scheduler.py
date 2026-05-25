from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)

from database import (
    get_connection
)

from config import (
    GROUP_CHAT_ID,
    TOPIC_ID,
    TIMEZONE
)


# ==========================
# CHECK AIRCONS
# ==========================

async def remind_aircons(
    bot
):

    conn = get_connection()

    c = conn.cursor()

    c.execute(
        """
        SELECT
        aircon_name,
        status
        FROM aircon_status
        """
    )

    rows = c.fetchall()

    conn.close()

    for row in rows:

        if (
            row["status"]
            != "ON"
        ):
            continue

        await (
            bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=(
                    "No one has turned "
                    "OFF the "
                    f"{row['aircon_name']} "
                    "yet.\n\n"
                    "Please do so."
                ),
                message_thread_id=TOPIC_ID
            )


# ==========================
# START
# ==========================

def start_scheduler(
    application
):

    async def start_job(
        app
    ):

        scheduler = (
            AsyncIOScheduler(
                timezone=TIMEZONE
            )
        )

        scheduler.add_job(
            remind_aircons,
            trigger="cron",
            hour=23,
            minute=59,
            kwargs={
                "bot":
                app.bot
            }
        )

        scheduler.start()

    application.post_init = start_job