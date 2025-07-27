from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboards.startkb as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"""Hi, {user_name}! 🤖 Welcome to Prompt Training Bot!\n
It’s 2025 — AI is everywhere. But smart results need smart prompts.\n
Sharpen your skills and become a true Prompt Master! """,
        reply_markup=kb.main,
    )
