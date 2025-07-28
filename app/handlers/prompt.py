import requests
import sqlite3
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import app.keyboards.backKb as backKb
import app.keyboards.promptkb as promptkb
import app.keyboards.startkb as startkb

router = Router()

class Prompt(StatesGroup):
    mode = State()
    text = State()

def request_to_mistral(mode: str, text: str):
    templates = {
        "🧠 Training": (
            "Analyze this prompt. If there are any shortcomings, explain them in simple words and suggest how it can be improved. "
            'If everything is fine, just say: "The prompt is of good quality, no improvements are needed." '
            "Do not invent shortcomings if there are none. Here is the text for analysis: {text}"
        ),
        "🖼️ Creation": (
            "Analyze this creative prompt. Focus on how clearly it inspires imagination, whether it gives enough direction for a creative task, "
            "and whether it's open-ended enough for artistic freedom. If there are any shortcomings, explain them simply and suggest how to improve "
            'the prompt to make it more creative or inspiring. If the prompt is already great, just say: "The prompt is of good quality, no improvements are needed." '
            "Do not invent flaws if there are none. Here is the prompt to analyze: {text}"
        ),
        "💻 Code": (
            "Analyze this coding-related prompt. Focus on how clearly the task is described, whether the technical requirements are well-defined, and if the goal is achievable and specific. "
            "If there are any shortcomings, explain them in simple terms and suggest how to improve the prompt to make it more precise or useful for generating code. "
            'If the prompt is already good, just say: "The prompt is of good quality, no improvements are needed." '
            "Do not invent flaws if there are none. Here is the text for analysis: {text}"
        ),
    }

    if mode not in templates:
        return "⚠️ Unknown mode selected."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": templates[mode].format(text=text),
                "stream": False,
            },
        )
        return response.json().get("response", "⚠️ No response returned.")
    except Exception as e:
        return f"⚠️ Failed to connect to the AI model: {str(e)}"

def init_db():
    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS History (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                mode TEXT NOT NULL,
                prompt TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)

@router.message(F.text == "🧠 Prompt training")
async def prompt_cmd(message: Message, state: FSMContext):
    await message.answer(text="Select the mode:", reply_markup=promptkb.promptButtons)
    await state.set_state(Prompt.mode)


@router.message(Prompt.mode)
async def handle_text(message: Message, state: FSMContext):
    await state.update_data(mode=message.text)
    await message.answer(
        text="Formulate the prompt according to the selected mode:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Prompt.text)


@router.message(Prompt.text)
async def handle_prompt(message: Message, state: FSMContext):
    user_data = await state.get_data()
    mode = user_data.get("mode")
    user_text = message.text
    await message.answer(
        "🔍 Analyzing your prompt, please wait (Warning! This may take up to 5 minutes.)..."
    )
    result = request_to_mistral(mode, user_text)
    await message.answer(result, reply_markup=backKb.backButton)
    await state.clear()

    init_db()

    with sqlite3.connect('app/database/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO History (mode, prompt) VALUES (?, ?)",
            (mode, user_text)
        )

@router.callback_query(F.data == "back_button")
async def back_to_menu(callback: CallbackQuery):
    username = callback.from_user.first_name
    await callback.message.answer(
        f"""Hi, {username}! 🤖 Welcome to Prompt Training Bot!\n
It’s 2025 — AI is everywhere. But smart results need smart prompts.\n
Sharpen your skills and become a true Prompt Master! """,
        reply_markup=startkb.main,
    )
    await callback.answer()