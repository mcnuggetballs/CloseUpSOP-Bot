from telegram import InlineKeyboardMarkup


async def show_screen(
    update,
    context,
    text,
    keyboard=None
):

    markup = None

    if keyboard:
        markup = InlineKeyboardMarkup(
            keyboard
        )

    message_id = context.user_data.get(
        "ui_message_id"
    )

    try:

        # callback → edit existing
        if (
            update.callback_query
            and update.callback_query.message
        ):

            msg = await (
                update.callback_query
                .message
                .edit_text(
                    text=text,
                    reply_markup=markup
                )
            )

            context.user_data[
                "ui_message_id"
            ] = msg.message_id

            return

        # reuse previous bot message
        if message_id:

            msg = await (
                context.bot
                .edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=message_id,
                    text=text,
                    reply_markup=markup
                )
            )

            context.user_data[
                "ui_message_id"
            ] = msg.message_id

            return

    except:
        pass

    # fallback → send new

    msg = await (
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=markup
        )
    )

    context.user_data[
        "ui_message_id"
    ] = msg.message_id