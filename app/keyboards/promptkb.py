from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

promptButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🧠 Training'), KeyboardButton(text='🖼️ Creation')], 
    [KeyboardButton(text='💻 Code')]
], resize_keyboard=True, input_field_placeholder='Select the parameter')