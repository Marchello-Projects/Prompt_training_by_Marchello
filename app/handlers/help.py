from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "❔ Help")
async def help_cmd(message: Message):
    await message.answer(
        "🆘 *Help Menu*\n\n"
        "Welcome to the AI Prompt Training Bot! 🤖\n"
        "This bot will help you master the art of writing effective prompts for AI.\n\n"
        "📌 Main commands:\n\n"
        "🧠 Prompt training — Start a training session. Choose a category (Custom prompt, Creative, Code, Homework) and create your prompt. You'll get feedback and suggestions from the AI.\n\n"
        "🕒 History — View your prompt history: previous prompts, scores, and feedback.\n\n"
        "❔ Help — Show this help message.\n\n"
        "🏆 Achievements — See your progress: skill level, best prompts, and personal stats.\n\n"
        "💡 Tip: The more detailed and clear your prompt is, the better the AI response will be. Practice makes perfect!",
    )
