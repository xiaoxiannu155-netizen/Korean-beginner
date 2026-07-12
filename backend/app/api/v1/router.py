from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.letters import router as letters_router
from app.api.v1.words import router as words_router
from app.api.v1.grammar import router as grammar_router
from app.api.v1.batchim import router as batchim_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.stats import router as stats_router
from app.api.v1.admin import router as admin_router
from app.api.v1.badges import router as badges_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.spelling import router as spelling_router
from app.api.v1.ai import router as ai_router
from app.api.v1.scenarios import router as scenarios_router
from app.api.v1.speech_eval import router as speech_eval_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(letters_router)
api_router.include_router(words_router)
api_router.include_router(grammar_router)
api_router.include_router(batchim_router)
api_router.include_router(tasks_router)
api_router.include_router(stats_router)
api_router.include_router(admin_router)
api_router.include_router(badges_router)
api_router.include_router(reviews_router)
api_router.include_router(spelling_router)
api_router.include_router(ai_router)
api_router.include_router(scenarios_router)
api_router.include_router(speech_eval_router)
