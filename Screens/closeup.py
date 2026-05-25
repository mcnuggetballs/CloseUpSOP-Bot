from telegram import (
    InlineKeyboardButton,
    InputMediaPhoto
)

from UI.show_screen import (
    show_screen
)

from UI.keyboards import (
    back_home,
    home_only
)

from constants import (
    CLOSEUP_STEPS
)

from Services import (
    closeup_service
)

from datetime import datetime


# ==========================
# ENTRY
# ==========================

async def confirm(
    update,
    context
):

    keyboard = [

        [
            InlineKeyboardButton(
                "Yes",
                callback_data="closeup_start"
            )
        ]

    ]

    keyboard.extend(
        back_home()
    )

    await show_screen(
        update,
        context,
        (
            "Are you closing up "
            "the venue and have "
            "you informed Luke?"
        ),
        keyboard
    )


# ==========================
# START
# ==========================

async def start(
    update,
    context
):

    context.user_data[
        "closeup_step"
    ] = 0

    context.user_data[
        "closeup_images"
    ] = []

    await render_step(
        update,
        context
    )


# ==========================
# RENDER
# ==========================

async def render_step(
    update,
    context
):

    step = (
        context
        .user_data[
            "closeup_step"
        ]
    )

    context.user_data[
        "screen"
    ] = (
        f"closeup_step"
    )

    prompt = (
        CLOSEUP_STEPS[
            step
        ]
    )

    # Saturday special rule
    if (
        step == 1
        and datetime.now().weekday() == 5
    ):

        prompt += (

            "\n\nSaturday Rule:\n"
            "Carpets and banners "
            "may remain out for "
            "Sunday classes."
        )

    text = (
        f"Step "
        f"{step+1}"
        f"/12\n\n"
        f"{prompt}"
    )

    await show_screen(
        update,
        context,
        text,
        back_home()
    )


# ==========================
# RECEIVE PHOTO
# ==========================

async def receive_step_photo(
    update,
    context
):

    photo = (
        update
        .message
        .photo[-1]
        .file_id
    )

    context.user_data[
        "closeup_images"
    ].append(
        photo
    )

    try:

        await (
            update
            .message
            .delete()
        )

    except:
        pass

    step = (
        context
        .user_data[
            "closeup_step"
        ]
    )

    if step == 11:

        await show_screen(
            update,
            context,
            (
                "⏳ Bot Uploading Images\n\n"
                "Please wait..."
            ),
            []
        )

        success = await (
            closeup_service
            .complete(
                update,
                context
            )
        )

        if success:

            await show_screen(
                update,
                context,
                (
                    "✅ Close Up Completed\n\n"
                    "All photos uploaded."
                ),
                home_only()
            )

        return

    context.user_data[
        "closeup_step"
    ] += 1

    await render_step(
        update,
        context
    )


# ==========================
# BACK
# ==========================

async def back(
    update,
    context
):

    step = (
        context
        .user_data
        .get(
            "closeup_step",
            0
        )
    )

    if step == 0:

        return

    context.user_data[
        "closeup_step"
    ] -= 1

    imgs = (
        context
        .user_data[
            "closeup_images"
        ]
    )

    if imgs:

        imgs.pop()

    await render_step(
        update,
        context
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

    if data == "closeup_start":

        await start(
            update,
            context
        )

        return