from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.generator import GeneratorResponse
from app.services.ai_generator import generate_from_chunks
from app.services.document_extractor import chunk_text, extract_text

router = APIRouter(prefix="/ai", tags=["AI Generation"])


@router.post("/generate", response_model=GeneratorResponse)
async def generate_study_materials(
    file: UploadFile = File(...),
    flashcard_count: int = Form(default=10, ge=1, le=50),
    quiz_count: int = Form(default=10, ge=1, le=50),
) -> GeneratorResponse:
    text, content_type = await extract_text(file)
    chunks = chunk_text(text)
    result = await generate_from_chunks(chunks, flashcard_count, quiz_count)
    return GeneratorResponse(filename=file.filename or "upload", content_type=content_type, characters_extracted=len(text), chunks_processed=len(chunks), result=result)