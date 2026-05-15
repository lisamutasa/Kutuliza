"""
app.py - Kutuliza Backend
"""

import io
import os
import base64
import tempfile
import mimetypes
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import mutagen

# FIXED IMPORTS - Direct import since we are inside backend folder
from backend.pipeline import (
    step_transcribe,
    step_summarise,
    step_translate,
    step_tts,
    LANGUAGE_NAMES,
    MAX_AUDIO_SECONDS,
)

load_dotenv()

app = FastAPI(
    title="Kutuliza API",
    description="AI-powered medical triage powered by Sunbird AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_AUDIO_TYPES = {
    "audio/mpeg", "audio/mp3", "audio/wav", "audio/wave",
    "audio/ogg", "audio/m4a", "audio/aac", "audio/x-m4a",
}
SUPPORTED_LANGUAGES = set(LANGUAGE_NAMES.keys())


def _audio_duration_seconds(path: Path) -> float | None:
    try:
        audio = mutagen.File(str(path))
        if audio is not None and audio.info:
            return audio.info.length
    except Exception:
        pass
    return None


def _audio_bytes_to_b64(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode("utf-8")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "kutuliza-api"}


class TextRequest(BaseModel):
    text: str
    target_language: str = "lug"


@app.post("/api/process/text")
async def process_text(body: TextRequest):
    if not body.text.strip():
        raise HTTPException(status_code=422, detail="Text input cannot be empty.")

    if body.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=422, detail=f"Unsupported language '{body.target_language}'.")

    try:
        summary = step_summarise(body.text)
        translation = step_translate(summary, body.target_language)
        audio_bytes = step_tts(translation, body.target_language)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Sunbird API error: {exc}")

    return JSONResponse({
        "transcript": None,
        "source_text": body.text,
        "summary": summary,
        "translation": translation,
        "audio_b64": _audio_bytes_to_b64(audio_bytes),
        "target_language": body.target_language,
        "target_language_name": LANGUAGE_NAMES[body.target_language],
    })


@app.post("/api/process/audio")
async def process_audio(
    audio: UploadFile = File(...),
    stt_language: str = Form("lug"),
    target_language: str = Form("lug"),
):
    if stt_language not in SUPPORTED_LANGUAGES and stt_language != "eng":
        raise HTTPException(status_code=422, detail=f"Unsupported STT language '{stt_language}'.")

    if target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=422, detail=f"Unsupported target language '{target_language}'.")

    # Save uploaded file temporarily
    suffix = Path(audio.filename or "audio.mp3").suffix or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await audio.read())
        tmp_path = Path(tmp.name)

    try:
        duration = _audio_duration_seconds(tmp_path)
        if duration is not None and duration > MAX_AUDIO_SECONDS:
            raise HTTPException(status_code=422, detail=f"Audio too long. Max 5 minutes.")

        transcript = step_transcribe(tmp_path, stt_language)
        summary = step_summarise(transcript)
        translation = step_translate(summary, target_language)
        audio_bytes = step_tts(translation, target_language)

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Sunbird API error: {exc}")
    finally:
        tmp_path.unlink(missing_ok=True)

    return JSONResponse({
        "transcript": transcript,
        "source_text": transcript,
        "summary": summary,
        "translation": translation,
        "audio_b64": _audio_bytes_to_b64(audio_bytes),
        "target_language": target_language,
        "target_language_name": LANGUAGE_NAMES[target_language],
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)