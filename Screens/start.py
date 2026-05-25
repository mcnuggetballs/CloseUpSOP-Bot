from Screens import menu


async def start(
    update,
    context
):

    keep = {

        "ui_message_id":
        context.user_data.get(
            "ui_message_id"
        )

    }

    context.user_data.clear()

    context.user_data.update(
        keep
    )

    context.user_data[
        "screen"
    ] = "menu"

    try:

        await (
            update
            .message
            .delete()
        )

    except:
        pass

    await menu.show(
        update,
        context
    )