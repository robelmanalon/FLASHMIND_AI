from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_UPLOAD_BYTES = 15 * 1024 * 1024


async def extract_text(upload: UploadFile) -> tuple[str, str]:
    extension = Path(upload.filename or "").suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Only PDF, DOCX, and TXT files are supported")
    content = await upload.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Files must be 15 MB or smaller")
    try:
        if extension == ".pdf":
            text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)
        elif extension == ".docx":
            text = "\n".join(paragraph.text for paragraph in Document(BytesIO(content)).paragraphs)
        else:
            text = content.decode("utf-8-sig")
    except Exception as error:
        raise HTTPException(status_code=422, detail=f"Could not extract text from {upload.filename}") from error
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip()).strip()
    if not text:
        raise HTTPException(status_code=422, detail="The uploaded file does not contain readable text")
    return text, upload.content_type or "application/octet-stream"


def chunk_text(text: str, max_characters: int = 12000, overlap: int = 500) -> list[str]:
    if len(text) <= max_characters:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_characters, len(text))
        boundary = text.rfind("\n", start, end)
        if boundary > start + max_characters // 2:
            end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks