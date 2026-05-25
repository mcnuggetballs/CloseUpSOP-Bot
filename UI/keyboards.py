from telegram import InlineKeyboardButton


def back_home():

    return [

        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="back"
            ),

            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]

    ]


def home_only():

    return [

        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]

    ]


def single_button(
    text,
    callback
):

    return [

        [
            InlineKeyboardButton(
                text,
                callback_data=callback
            )
        ]

    ]


def rows(*buttons):

    keyboard = []

    for row in buttons:

        keyboard.append(row)

    return keyboard