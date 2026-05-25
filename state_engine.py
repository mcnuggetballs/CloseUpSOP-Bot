from Screens import menu, aircon, closeup


def clear_flow(context):

    keep = {
        "ui_message_id": context.user_data.get("ui_message_id")
    }

    context.user_data.clear()

    context.user_data.update(keep)


async def go_home(
    update,
    context
):

    context.user_data.pop(
        "closeup_images",
        None
    )

    context.user_data.pop(
        "closeup_step",
        None
    )

    clear_flow(
        context
    )

    context.user_data[
        "screen"
    ] = "menu"

    await menu.show(
        update,
        context
    )


# ==========================
# TEXT INPUT
# ==========================

async def handle_text(
    update,
    context
):

    if (
        update.effective_chat.type
        ==
        "private"
    ):

        try:

            await (
                update
                .message
                .delete()
            )

        except:
            pass

    screen = (
        context
        .user_data
        .get(
            "screen"
        )
    )

    if screen == "idle":
        return

    if screen == "unused":
        return


# ==========================
# PHOTO INPUT
# ==========================

async def handle_photo(update, context):

    screen = context.user_data.get("screen")

    try:
        await update.message.delete()
    except:
        pass

    if screen == "aircon_off_photo":
        await aircon.receive_off_photo(
            update,
            context
        )
        return

    if screen.startswith("closeup_step"):
        await closeup.receive_step_photo(
            update,
            context
        )
        return


# ==========================
# CALLBACK
# ==========================

async def handle_callback(update, context):

    query = update.callback_query

    await query.answer()

    data = query.data

    screen = context.user_data.get("screen")

    # -----------------
    # HOME
    # -----------------

    if data == "home":

        await go_home(
            update,
            context
        )

        return

    # -----------------
    # BACK
    # -----------------

    if data == "back":
        if (
            screen
            ==
            "aircon_off_photo"
        ):

            await (
                aircon
                .go_back(
                    update,
                    context
                )
            )

            return
        if (
            screen
            ==
            "closeup_step"
        ):

            await (
                closeup
                .back(
                    update,
                    context
                )
            )

            return
        previous = context.user_data.get(
            "previous_screen"
        )

        if previous:

            context.user_data["screen"] = previous

        await menu.route(
            update,
            context
        )

        return

    # -----------------
    # MENU
    # -----------------

    if data == "menu_aircon":

        context.user_data[
            "previous_screen"
        ] = screen

        context.user_data[
            "screen"
        ] = "aircon_select"

        await aircon.select_aircon(
            update,
            context
        )

        return

    if data == "menu_closeup":

        context.user_data[
            "previous_screen"
        ] = screen

        context.user_data[
            "screen"
        ] = "closeup_confirm"

        await closeup.confirm(
            update,
            context
        )

        return

    # -----------------
    # AIRCON
    # -----------------

    if (
        data.startswith(
            "aircon_select|"
        )
        or
        data.startswith(
            "aircon_action|"
        )
    ):

        await aircon.handle_callback(
            update,
            context
        )

        return

    # -----------------
    # CLOSEUP
    # -----------------

    if (
        data.startswith(
            "closeup"
        )
    ):

        await closeup.handle_callback(
            update,
            context
        )

        return