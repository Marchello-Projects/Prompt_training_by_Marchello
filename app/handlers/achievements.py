from aiogram import F, Router
from aiogram.types import Message

from app.handlers.prompt import score

router = Router()

templates = {
    10: "🤖 Prompt Rookie",
    25: "🧠 AI Apprentice",
    50: "🚀 Prompt Pro",
    100: "🌐 Master of AI",
}


def check_level(points):
    eligible_levels = [score for score in templates.keys() if points >= score]
    if not eligible_levels:
        return "👶 Newbie"

    max_score = max(eligible_levels)
    return templates[max_score]


@router.message(F.text == "🏆 Achievements")
async def show_achievements(message: Message):
    points = score.get_points()
    level = check_level(points=points)

    await message.answer(
        f"Your current level: {level}\n\n"
        "Levels:\n"
        "👶 Beginner - given immediately\n"
        "🤖 Prompt Rookie - given when you reach 10 points\n"
        "🧠 AI Apprentice - given when you reach 25 points\n"
        "🚀 Prompt Pro - given when you reach 50 points\n"
        "🌐 Master of AI - given when you reach 100 points\n\n"
        "Complete a prompt – earn a point!"
    )
