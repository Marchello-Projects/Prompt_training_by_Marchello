from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🧠 Prompt training'), KeyboardButton(text='❔ Help')], 
    [KeyboardButton(text='🕒 Prompts training history'), KeyboardButton(text='🏆 Achievements')]
], resize_keyboard=True)