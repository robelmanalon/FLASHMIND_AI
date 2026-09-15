from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.health import HealthResponse
from app.api import auth, decks, generator, profile, quiz, stats, study

app = FastAPI(title="FlashMind AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    # Vite may move to the next available port when another dev server is running.
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(decks.router)
app.include_router(quiz.router)
app.include_router(study.router)
app.include_router(generator.router)
app.include_router(stats.router)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="flashmind-api")