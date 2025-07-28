from .achievements import router as achievements_router
from .help import router as help_router
from .history import router as history_router
from .prompt import router as prompt_router
from .start import router as start_router

routers = [
    start_router,
    help_router,
    prompt_router,
    history_router,
    achievements_router,
]
