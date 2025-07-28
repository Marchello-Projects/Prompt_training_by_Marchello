from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

promptButtons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 Custom prompt"), KeyboardButton(text="🎨 Creative")],
        [KeyboardButton(text="💻 Code"), KeyboardButton(text="📚 Homework")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose the prompt type:",
)
