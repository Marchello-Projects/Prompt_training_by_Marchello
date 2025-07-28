from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Prompt training"), KeyboardButton(text="❔ Help")],
        [KeyboardButton(text="🕒 History"), KeyboardButton(text="🏆 Achievements")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Select the parameter",
)
