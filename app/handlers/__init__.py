from .help import router as help_router
from .start import router as start_router
from .prompt import router as prompt_router

routers = [start_router, help_router, prompt_router]
