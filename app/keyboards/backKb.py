from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

backButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to main menu", callback_data="back_button")]
    ]
)
