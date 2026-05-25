from telegram import InlineKeyboardButton

from UI.show_screen import show_screen
from UI.keyboards import (
    back_home,
    home_only
)

from constants import AIRCONS

from Services import aircon_service


# ==========================
# SELECT AIRCON
# ==========================

async def select_aircon(
    update,
    context
):

    keyboard = []

    for aircon in AIRCONS:

        keyboard.append([
            InlineKeyboardButton(
                aircon,
                callback_data=f"aircon_select|{aircon}"
            )
        ])

    keyboard.extend(
        back_home()
    )

    await show_screen(
        update,
        context,
        "Select Aircon",
        keyboard
    )


# ==========================
# ACTION
# ==========================

async def select_action(
    update,
    context
):

    keyboard = [

        [
            InlineKeyboardButton(
                "ON",
                callback_data="aircon_action|ON"
            )
        ],

        [
            InlineKeyboardButton(
                "OFF",
                callback_data="aircon_action|OFF"
            )
        ]

    ]

    keyboard.extend(
        back_home()
    )

    await show_screen(
        update,
        context,
        "Select Action",
        keyboard
    )


# ==========================
# REQUEST PHOTO
# ==========================

async def request_off_photo(
    update,
    context
):

    context.user_data[
        "screen"
    ] = "aircon_off_photo"

    await show_screen(
        update,
        context,
        (
            "Please send a photo proof "
            "that the aircon has "
            "been switched OFF."
        ),
        back_home()
    )


# ==========================
# RECEIVE PHOTO
# ==========================

async def receive_off_photo(
    update,
    context
):

    photo = (
        update.message
        .photo[-1]
        .file_id
    )

    success = await aircon_service.turn_off(
        update,
        context,
        photo
    )

    if success is False:

        await show_screen(
            update,
            context,
            "⚠ Aircon already OFF",
            home_only()
        )

        return

    await show_screen(
        update,
        context,
        "✅ Aircon switched OFF",
        home_only()
    )


# ==========================
# CALLBACK
# ==========================

async def handle_callback(
    update,
    context
):

    data = (
        update
        .callback_query
        .data
    )

    if data.startswith(
        "aircon_select|"
    ):

        selected = (
            data
            .split("|")[1]
        )

        context.user_data[
            "selected_aircon"
        ] = selected

        context.user_data[
            "screen"
        ] = "aircon_action"

        await select_action(
            update,
            context
        )

        return

    if data.startswith(
        "aircon_action|"
    ):

        action = (
            data
            .split("|")[1]
        )

        if action == "ON":

            success = await (
                aircon_service
                .turn_on(
                    update,
                    context
                )
            )

            if success is False:

                await show_screen(
                    update,
                    context,
                    "⚠ Aircon already ON",
                    home_only()
                )

                return

            await show_screen(
                update,
                context,
                "✅ Aircon switched ON",
                home_only()
            )

            return

        await request_off_photo(
            update,
            context
        )

async def go_back(
    update,
    context
):

    screen = (
        context
        .user_data
        .get(
            "screen"
        )
    )

    if (
        screen
        ==
        "aircon_off_photo"
    ):

        context.user_data[
            "screen"
        ] = (
            "aircon_action"
        )

        await select_action(
            update,
            context
        )