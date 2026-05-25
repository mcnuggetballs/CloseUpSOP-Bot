from telegram import InlineKeyboardButton
from UI.show_screen import show_screen


async def show(update, context):

    context.user_data["screen"] = "menu"

    keyboard = [

        [
            InlineKeyboardButton(
                "❄ Aircon Procedure",
                callback_data="menu_aircon"
            )
        ],

        [
            InlineKeyboardButton(
                "🏁 Close Up Procedure",
                callback_data="menu_closeup"
            )
        ]
    ]

    text = """
Facility Bot

Select a procedure.
"""

    await show_screen(
        update,
        context,
        text,
        keyboard
    )


async def route(update, context):

    screen = context.user_data.get(
        "screen"
    )

    if screen == "menu":

        await show(
            update,
            context
        )

        return

    await show(
        update,
        context
    )