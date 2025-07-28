from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

backButton = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Back to main menu', callback_data='back_button')]
])