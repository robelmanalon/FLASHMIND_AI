import asyncio
import json

import google.generativeai as genai
from fastapi import HTTPException

from app.config import settings
from app.schemas.generator import GeneratedContent


def _model() -> genai.GenerativeModel:
    if not settings.gemini_api_key or settings.gemini_api_key == "your-gemini-api-key":
        raise HTTPException(status_code=503, detail="Gemini is not configured. Set GEMINI_API_KEY in backend/.env and restart FastAPI.")
    genai.configure(api_key=settings.gemini_api_key)
    return genai.GenerativeModel(settings.gemini_model)


def _generate(model: genai.GenerativeModel, prompt: str):
    return model.generate_content(prompt, generation_config={"temperature": 0.25, "response_mime_type": "application/json"})


MAX_ATTEMPTS = 3


async def generate_from_chunks(chunks: list[str], flashcard_count: int = 10, quiz_count: int = 10) -> GeneratedContent:
    schema = json.dumps(GeneratedContent.model_json_schema(), indent=2)
    source = '\n\n--- DOCUMENT CHUNK ---\n\n'.join(chunks)
    model = _model()
    feedback = ""
    for attempt in range(MAX_ATTEMPTS):
        prompt = f"""Create accurate study materials from the source text below. Never invent facts.
Return only valid JSON matching this schema:
{schema}

Generate EXACTLY {flashcard_count} flashcards and EXACTLY {quiz_count} quiz questions. The final JSON MUST contain
exactly {flashcard_count} entries in "flashcards" and exactly {quiz_count} entries in "quiz_questions" - no fewer.
Include multiple-choice, true-false, and identification questions when supported.
Use an empty string for explanations when none is needed and an empty options array for non-choice questions.

SOURCE TEXT:
{source}"""
        if feedback:
            prompt = f"{feedback}\n\nFix ONLY the counts in your previous answer, keep the same quality, and return the corrected full JSON.\n\nReturn valid JSON matching this schema:\n{schema}\n\nSOURCE TEXT:\n{source}"
        try:
            response = await asyncio.to_thread(_generate, model, prompt)
        except Exception as error:
            message = str(error).lower()
            if "api key" in message or "authentication" in message or "401" in message or "403" in message:
                raise HTTPException(status_code=502, detail="Gemini rejected the API key. Check GEMINI_API_KEY in backend/.env.") from error
            if "quota" in message or "429" in message or "resource exhausted" in message:
                raise HTTPException(status_code=429, detail="Gemini quota or rate limit reached. Check your Google AI Studio quota and try again later.") from error
            raise HTTPException(status_code=502, detail="Gemini generation failed. Check GEMINI_API_KEY, GEMINI_MODEL, and API quota.") from error
        content = getattr(response, "text", None)
        if not content:
            raise HTTPException(status_code=502, detail="Gemini returned an empty response")
        try:
            parsed = GeneratedContent.model_validate(json.loads(content))
        except (ValueError, TypeError) as error:
            raise HTTPException(status_code=502, detail="Gemini returned invalid structured JSON") from error
        flashcards_missing = flashcard_count - len(parsed.flashcards)
        quizzes_missing = quiz_count - len(parsed.quiz_questions)
        if flashcards_missing <= 0 and quizzes_missing <= 0:
            return GeneratedContent(
                flashcards=parsed.flashcards[:flashcard_count],
                quiz_questions=parsed.quiz_questions[:quiz_count],
            )
        feedback = (
            f"Your previous answer had {len(parsed.flashcards)} flashcards and {len(parsed.quiz_questions)} quiz "
            f"questions. You MUST return exactly {flashcard_count} flashcards and exactly {quiz_count} quiz questions."
        )
    return GeneratedContent(
        flashcards=parsed.flashcards[:flashcard_count],
        quiz_questions=parsed.quiz_questions[:quiz_count],
    )